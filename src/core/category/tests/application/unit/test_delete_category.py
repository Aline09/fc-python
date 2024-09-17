
from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        # 3 passos: arrange, execução e asserção
        category = Category(
            name="Filme",
            description="Categoria de Filmes"
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)

        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(category.id) 

    def test_when_category_not_found_then_raise_exception(self):
        not_found_id = uuid4()
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(mock_repository)

        with pytest.raises(CategoryNotFound, match=f'Category {not_found_id} Not Found'): 
            use_case.execute(DeleteCategoryRequest(id=not_found_id))
        
        mock_repository.delete.assert_not_called()

        