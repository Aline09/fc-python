from uuid import UUID, uuid4
from django.urls import reverse
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
        
        url =  url = f'/api/categories/{category_documentary.id}/'
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
        url =  url = f'/api/categories/{uuid4()}/'
        
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