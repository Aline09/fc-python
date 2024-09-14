from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

from uuid import UUID, uuid4
class TestInMemoryCategoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme",
            description="Categoria para filmes",
        )

        repository.save(category=category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

class TestGetById:
    def test_return_found_category(self):
        my_category = Category(name="Filmes", description="Categoria para Filmes", is_active=True)
        repository = InMemoryCategoryRepository(categories=[my_category])
        response = repository.get_by_id(id=my_category.id)

        assert response == my_category
    
    def test_raise_error_when_category_is_not_found(self):
        my_category = Category(name="Filmes", description="Categoria para Filmes", is_active=True)
        repository = InMemoryCategoryRepository(categories=[my_category])
        not_found_id = uuid4()
        response = repository.get_by_id(id=not_found_id)

        assert response is None