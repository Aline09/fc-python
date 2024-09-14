from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(name="Filmes", description="Categoria de Filmes", is_active=True)
        repository = InMemoryCategoryRepository(categories=[category])
        repository.save(category=category)
        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(id=category.id, name="Filmes Novo", description="Categoria de Filmes Novo")

        use_case.execute(request=request)

        updated_category = repository.get_by_id(category.id)

        assert updated_category.name == 'Filmes Novo'
        assert updated_category.description == 'Categoria de Filmes Novo'