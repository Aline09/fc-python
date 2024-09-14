from unittest.mock import create_autospec
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import ListCategoryRequest, ListCategoryResponse, ListCategory, CategoryOutput
from src.core.category.domain.category import Category
from src.core.category.tests.domain.test_category import TestCategory


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        category = Category(name="Filmes", description="Categoria para Filmes")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []
        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert response == ListCategoryResponse(data=[])

    def test_when_categories_in_repository_then_return_list(self):
        category_filme = Category(name="Filmes", description="Categoria para Filmes")
        category_serie = Category(name="Serie", description="Categoria para Séries")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category_filme, category_serie]
        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert response == ListCategoryResponse(
                data=[
                    CategoryOutput(
                        id=category_filme.id, 
                        name=category_filme.name, 
                        description=category_filme.description, 
                        is_active=category_filme.is_active
                    ),
                     CategoryOutput(
                        id=category_serie.id, 
                        name=category_serie.name, 
                        description=category_serie.description, 
                        is_active=category_serie.is_active
                    )
                ]
            )