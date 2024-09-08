import pytest
import unittest
from uuid import UUID, uuid4 # std library  - ja vem instalado com o python

from src.core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_cannot_create_category_with_empty_name(self):
         with pytest.raises(ValueError, match="Cannot create category with empty name"):
              Category(name="")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 255 characteres"):
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

# Cada classe de teste responsável por uma método e cada função dentro do método responsável por um edge case
class TestUpdateCategory: 
     def test_update_category_with_name_and_description(self):
         category = Category(name="Filme", description="Filmes em geral")

         category.update_category(name="Série", description="Séries em geral")

         assert category.name == "Série"
         assert category.description == "Séries em geral"

     def test_update_category_with_invalid_name(self):
          category = Category(name = "Filmes")
          with pytest.raises(ValueError, match="name must have less than 255 characteres"):
               category.update_category(name ="a" * 256, description="Minha nova descrição")

     def test_cannot_update_category_with_empty_name(self):
         with pytest.raises(ValueError, match="Cannot create category with empty name"):
              Category(name="")

     def test_activate_inactive_category(self):
          category = Category(
               name="Filme", 
               description="Filmes em geral", 
               is_active=True
          )
          
          category.activate_category()
          
          assert category.is_active is True
     
     def test_activate_active_category(self): # Teste para verificar se ativar uma categoria é independente do valor anterior dela
          category = Category(
               name="Filme", 
               description="Filmes em geral", 
          )
          
          category.activate_category()
          
          assert category.is_active is True

     def test_deactivate_active_category(self):
          category = Category(name="Séries", description="Minhas Séries", is_active=True)

          category.deactivate_category()

          assert category.is_active is False

     def test_deactivate_inactive_category(self):
          category = Category(name="Séries", description="Minhas Séries", is_active=False)

          category.deactivate_category()

          assert category.is_active is False

class TestEquality:
     def test_when_categories_have_same_id_they_are_equal(self):
          common_id = uuid4()
          category_1 = Category(name="Filme", id=common_id)
          category_2 = Category(name="Filme", id=common_id)
          assert category_1 == category_2

     def test_equality_different_classes(self):
          class Dummy:
               pass

          common_id = uuid4()

          category = Category(name="Filmes", id=common_id)
          dummy = Dummy()
          dummy.id = common_id

          assert category != dummy