from dataclasses import dataclass
from uuid import UUID

# Application depende de domain
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.category_repository import CategoryRepository
# from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository - não importamos mais de um módulo de nível mais baixo

@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, request: DeleteCategoryRequest):
        category = self.repository.get_by_id(id=request.id)
       
        if category is None:
            raise CategoryNotFound(f'Category {request.id} Not Found')
        
        self.repository.delete(category.id)
        
        return None
