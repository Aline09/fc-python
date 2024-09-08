from uuid import UUID

import pytest
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(name="Filmes", description="Categoria de Filmes", is_active=True)
        response = use_case.execute(request=request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].id == response.id
        assert repository.categories[0].name == 'Filmes'
        assert repository.categories[0].description == 'Categoria de Filmes'
        assert repository.categories[0].is_active is True
        # assert repository.save.called is True

    def test_create_category_with_invalid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(name="")
        with pytest.raises(InvalidCategoryData, match="Cannot create category with empty name") as exc_info: 
            use_case.execute(request=request)
       
           
        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "Cannot create category with empty name"
        assert len(repository.categories) == 0