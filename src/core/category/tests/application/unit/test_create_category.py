from unittest.mock import MagicMock
from uuid import UUID

import pytest

# from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest, InvalidCategoryData


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository=MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="Filmes", description="Categoria de Filmes", is_active=True)
        response = use_case.execute(request=request)

        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_data(self):
        mock_repository=MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="")
        with pytest.raises(InvalidCategoryData, match="Cannot create category with empty name") as exc_info: 
            use_case.execute(request=request)
       
           
        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "Cannot create category with empty name"