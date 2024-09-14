from unittest.mock import create_autospec
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from uuid import uuid4


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            id=uuid4(), 
            name="Filmes", 
            description="Categoria para Filmes", 
            is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, name="Série")
        use_case.execute(request=request)

        assert category.name == 'Série'
        assert category.description == 'Categoria para Filmes'
        mock_repository.update.assert_called_once_with(category)


    def test_update_category_description(self):
        category = Category(
            id=uuid4(), 
            name="Filmes", 
            description="Categoria para Filmes Novo", 
            is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, description="Série")
        use_case.execute(request=request)

        assert category.name == 'Filmes'
        assert category.description == 'Série'
        mock_repository.update.assert_called_once_with(category)

    def test_update_deactivate_category(self):
        category = Category(
            id=uuid4(), 
            name="Filmes", 
            description="Filmes Novo", 
            is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=False)
        use_case.execute(request=request)

        assert category.name == 'Filmes'
        assert category.description == 'Filmes Novo'
        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_update_activate_category(self):
        category = Category(
            id=uuid4(), 
            name="Filmes", 
            description="Filmes Novo", 
            is_active=False)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=True)
        use_case.execute(request=request)

        assert category.name == 'Filmes'
        assert category.description == 'Filmes Novo'
        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)