from uuid import UUID, uuid4
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django_project.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category


@pytest.fixture
def category_movie():
    return  Category(
        name="Movie",
        description="Movie description",
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = '/api/categories/'
        response = APIClient().get(url)

        expected_data = { 
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True
                },
                {
                    "id": str(category_documentary.id),
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True
                }
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data

@pytest.mark.django_db
class TestRetrieveAPI:
    
    def test_when_id_is_invalid_return_400(self):
        url = '/api/categories/1234533/'

        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_return_category_when_exists(    
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) ->  None:
        category_repository.save(category=category_movie)
        category_repository.save(category=category_documentary)
        
        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().get(url)

        expected_data = {
            "data": {
                    "id": str(category_documentary.id),
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True
                }
            }
        

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_not_exists(self):
        url = f'/api/categories/{uuid4()}/'
        
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        assert response.data is None


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = '/api/categories/'

        response = APIClient().post(url, 
            data={
                "name": "",
                "description": "Movie Description"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."]
        }
    
    def test_when_payload_is_valid_than_create_category_and_return_201(self, category_repository: DjangoORMCategoryRepository) -> None:
        url = '/api/categories/'

        response = APIClient().post(url, 
            data={
                "name": "Movie Category",
                "description": "Movie Category Description"
            }
        )

        created_category_id = UUID(response.data["id"])
        assert response.status_code == status.HTTP_201_CREATED
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Movie Category",
            description="Movie Category Description"
        )

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = '/api/categories/12346/'
        data = {
            "name": "",
            "description": "Movie description",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        }


    # def test_when_payload_is_valid_than_create_category_and_return_201(self, category_repository: DjangoORMCategoryRepository) -> None:
    #     url = '/api/categories/'

    #     response = APIClient().post(url, 
    #         data={
    #             "name": "Movie Category",
    #             "description": "Movie Category Description"
    #         }
    #     )

    #     created_category_id = UUID(response.data["id"])
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert category_repository.get_by_id(created_category_id) == Category(
    #         id=created_category_id,
    #         name="Movie Category",
    #         description="Movie Category Description"
    #     )
        
    def test_when_category_does_not_exist_then_return_404(self):
        url = f'/api/categories/{uuid4()}/'

        data = {
            "name": "My Movie Category",
            "description": "Movie description",
            "is_active": True
        }
        
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = '/api/categories/12346/'
        
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_when_category_does_not_exist_then_return_404(self):
        url = f'/api/categories/{uuid4()}/'
        
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_does_exist_then_return_204(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category=category_movie)

        url = f'/api/categories/{category_movie.id}/'

        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.get_by_id(category_movie.id) is None
        assert category_repository.list() == []

@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = '/api/categories/12346/'
        
        data = {
            "name": "My Movie Category",
            "description": "Movie description",
            "is_active": True
        }
        response = APIClient().patch(url,data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_only_category_name(self):
        
        url = '/api/categories/'

        created_category = APIClient().post(url, data={
             "name": "Movie",
             "description": "Movie description",
        })

        created_category_id = created_category.data["id"]

        retrieved_category_url = f'/api/categories/{created_category_id}/'

        response = APIClient().get(retrieved_category_url)

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "Movie description",
                "is_active": True
            }
        }

        update_name = APIClient().patch(
            f'/api/categories/{created_category_id}/',
            data={"name": "My New Category Name"}
        )


        response = APIClient().get(retrieved_category_url)
        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": created_category_id,
                "name": "My New Category Name",
                "description": "Movie description",
                "is_active": True
            }
        }

    def test_update_only_category_description(self):
        url = '/api/categories/'

        created_category = APIClient().post(url, data={
             "name": "Movie",
             "description": "Movie description",
        })

        created_category_id = created_category.data["id"]

        retrieved_category_url = f'/api/categories/{created_category_id}/'

        response = APIClient().get(retrieved_category_url)

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "Movie description",
                "is_active": True
            }
        }

        update_name = APIClient().patch(
            f'/api/categories/{created_category_id}/',
            data={"description": "My New Category Description"}
        )


        response = APIClient().get(retrieved_category_url)
        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "My New Category Description",
                "is_active": True
            }
        }

    def test_update_only_category_status(self):
        url = '/api/categories/'

        created_category = APIClient().post(url, data={
             "name": "Movie",
             "description": "Movie description",
             "is_active": False
        })

        created_category_id = created_category.data["id"]

        retrieved_category_url = f'/api/categories/{created_category_id}/'

        response = APIClient().get(retrieved_category_url)

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "Movie description",
                "is_active": False
            }
        }

        update_name = APIClient().patch(
            f'/api/categories/{created_category_id}/',
            data={"is_active": True}
        )


        response = APIClient().get(retrieved_category_url)
        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "Movie description",
                "is_active": True
            }
        }