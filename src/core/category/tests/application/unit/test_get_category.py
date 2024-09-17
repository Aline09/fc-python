from unittest.mock import create_autospec

# from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse


class TestGetCategory:
    def test_return_found_category(self):
        category = Category(name="Filmes", description="Categoria para Filmes", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)
        response = use_case.execute(request=request)

        assert response == GetCategoryResponse(name="Filmes", description="Categoria para Filmes", id=category.id, is_active=True)

    # def test_create_category_with_invalid_data(self):
    #     mock_repository=MagicMock(CategoryRepository)
    #     use_case = CreateCategory(repository=mock_repository)
    #     request = CreateCategoryRequest(name="")
    #     with pytest.raises(InvalidCategoryData, match="Cannot create category with empty name") as exc_info: 
    #         use_case.execute(request=request)
       
           
    #     assert exc_info.type is InvalidCategoryData
    #     assert str(exc_info.value) == "Cannot create category with empty name"