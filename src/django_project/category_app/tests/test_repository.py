import pytest
from django_project.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category
from django_project.category_app.models import Category as CategoryModel



@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie Description"
        )

        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0

        repository.save(category=category)

        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()

        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active