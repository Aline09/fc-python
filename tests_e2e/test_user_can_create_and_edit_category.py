import pytest

from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()

        # Verifica que list esta vazia

        list_response = api_client.get('/api/categories/')

        assert list_response.data == {"data": []}

        # Criar uma categoria

        data = {
            "name": "Movies Category",
            "description": "My Movies Category"
        }
        
        create_response = api_client.post('/api/categories/', data=data)

        assert create_response.status_code == 201

        created_category_id = create_response.data["id"]

        # Verifica que list esta vazia

        list_response = api_client.get('/api/categories/')

        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movies Category",
                    "description": "My Movies Category",
                    "is_active": True
                }
            ]
        }

        # Edita Categoria Criada

        updated_data = {
                    "name": "Documentaries Category",
                    "description": "My Documentaries Category",
                    "is_active": False
                }
        
        update_response = api_client.put(f'/api/categories/{created_category_id}/', data=updated_data)

        assert update_response.status_code == 204
        
        list_response = api_client.get('/api/categories/')

        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Documentaries Category",
                    "description": "My Documentaries Category",
                    "is_active": False
                }
            ]
        }

        


