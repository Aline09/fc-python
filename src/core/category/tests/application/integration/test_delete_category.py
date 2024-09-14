from uuid import UUID, uuid4

import pytest
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.delete_category import DeleteCategoryRequest, DeleteCategory
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_filme = Category(name="Filmes", description="Categoria de Filmes", is_active=True)
        category_serie = Category(name="Séries", description="Categoria de Séries", is_active=True)
        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_filme.id)

        assert repository.get_by_id(category_filme.id) is not None
        response = use_case.execute(request=request)
        
        assert repository.get_by_id(category_filme.id) is None
        assert response is None