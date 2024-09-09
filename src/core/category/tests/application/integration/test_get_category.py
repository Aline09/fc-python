from uuid import UUID, uuid4

import pytest
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_get_category_by_id(self):
        category_filme = Category(name="Filmes", description="Categoria de Filmes", is_active=True)
        category_serie = Category(name="Séries", description="Categoria de Séries", is_active=True)
        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_filme.id)
        response = use_case.execute(request=request)

        assert response == GetCategoryResponse(
            id=category_filme.id,
            name="Filmes",
            description="Categoria de Filmes",
            is_active=True
        )
        # assert repository.save.called is True

    def test_when_category_does_not_exist_then_raise_exception(self):
        not_found_id = uuid4()
        category_filme = Category(name="Filmes", description="Categoria de Filmes", is_active=True)
        repository = InMemoryCategoryRepository(categories=[category_filme])
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound, match=f'Category {not_found_id} Not Found'): 
            use_case.execute(request=request)
        
        
       
