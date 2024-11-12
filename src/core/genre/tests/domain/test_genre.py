import pytest
from uuid import UUID, uuid4

from src.core.genre.domain.genre import Genre


class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_cannot_create_genre_with_empty_name(self):
         with pytest.raises(ValueError, match="Cannot create genre with empty name"):
              Genre(name="")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 255 characteres"):
            Genre(name = "a" * 256)
    
    def test_genre_must_be_created_with_id_as_uuid(self):
            genre = Genre(name="Terror")
            assert isinstance(genre.id, UUID)

    def test_create_genre_with_default_values(self):
         genre = Genre(name="Animação")
         assert genre.name == "Animação"
         assert genre.is_active is True
         assert isinstance(genre.id, UUID)
         assert genre.categories == set()

    
    def test_genre_is_created_with_provided_values(self):
         categories = {uuid4(), uuid4()}
         id = uuid4()
         genre = Genre(name="Suspense", is_active=False, id=id, categories=categories)
         
         assert genre.name == "Suspense"
         assert genre.id == id
         assert genre.is_active is False
         assert len(genre.categories) == 2 
         assert genre.categories == categories


    def test_show_genre_as_string(self):
         id = uuid4()
         genre = Genre(name="Terror", id=id)
         assert str(genre) == f"{genre.name} - ({genre.is_active})"
    
    def test_show_genre_representation(self):
         id = uuid4()
         genre = Genre(name="Suspense", id=id)
         assert repr(genre) == f"<Genre {genre.name} ({genre.id})>"

# Cada classe de teste responsável por uma método e cada função dentro do método responsável por um edge case
class TestActivate: 
     def test_activate_inactive_category(self):
          genre = Genre(
               name="Ação", 
               is_active=False
          )
          
          genre.activate()
          
          assert genre.is_active is True
     
     def test_activate_active_genre(self): # Teste para verificar se ativar uma categoria é independente do valor anterior dela
          genre = Genre(
               name="Ação", 
                
          )
          
          genre.activate()
          
          assert genre.is_active is True

     def test_deactivate_active_genre(self):
          genre = Genre(name="Terror", is_active=True)

          genre.deactivate()

          assert genre.is_active is False

     def test_deactivate_inactive_genre(self):
          genre = Genre(name="Comédia", is_active=False)

          genre.deactivate()

          assert genre.is_active is False

class TestEquality:
     def test_when_genres_have_same_id_they_are_equal(self):
          common_id = uuid4()
          genre_1 = Genre(name="Romance", id=common_id)
          genre_2 = Genre(name="Romance", id=common_id)
          assert genre_1 == genre_2

     def test_equality_different_classes(self):
          class Dummy:
               pass

          common_id = uuid4()

          genre = Genre(name="Filmes", id=common_id)
          dummy = Dummy()
          dummy.id = common_id

          assert genre != dummy

class TestChangeName:
     def test_change_name(self):
          genre = Genre(name="Suspense")
          genre.change_name(name="Suspense Novo")

          assert genre.name == "Suspense Novo"

     def test_name_is_empty(self):
          genre = Genre(name="Terror")
          
          with pytest.raises(ValueError, match="Cannot create genre with empty name"):
               genre.change_name(name="")

class TestAddCategory:
     def test_add_category(self):
          categories = {uuid4(), uuid4()}
          genre = Genre(name="Romance")

          for category_id in categories:
               assert category_id not in genre.categories
               
          for category_id in categories:
               genre.add_category(category_id)
          
          assert genre.categories == categories

        
     