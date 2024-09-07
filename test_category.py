import pytest
import unittest
from uuid import UUID, uuid4 # std library  - ja vem instalado com o python

from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, "name must have less than 256 characteres"):
            Category(name = "a" * 256)
    
    def test_category_must_be_create_with_id_as_uuid(self):
            category = Category(name="Filme")
            assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
         category = Category(name="Filme")

         assert category.name == "Filme"
         assert category.description == ""
         assert category.is_active is True # Quando queremos testar valores comoTrue, False ou None usamos is para fazer um teste de identidade
       

    def test_category_is_created_as_active_by_default(self):
         category = Category(name="Documentário")
         assert category.is_active is True
    
    def test_category_is_created_with_provided_values(self):
         id = uuid4()
         category = Category(name="Novelas")
         category.id = id
         category.description = "Novelas da Globo"
         category.is_active = False


         assert category.name == "Novelas"
         assert category.description ==  "Novelas da Globo"
         assert category.id == id
         assert category.is_active is False

    def test_show_category_as_string(self):
         id = uuid4()
         category = Category(name="Séries", id=id, description="Séries americanas")
         assert str(category) == f"{category.name} - {category.description} - ({category.is_active})"
    
    def test_show_category_representation(self):
         id = uuid4()
         category = Category(name="Séries", id=id)
         assert repr(category) == f"<Category {category.name} ({category.id})>"


if __name__ == "__main__":
    unittest.main()