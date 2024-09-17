from dataclasses import dataclass
from uuid import UUID

# Application depende de domain
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository
# from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository - não importamos mais de um módulo de nível mais baixo

@dataclass
class GetCategoryRequest:
    id: UUID

@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool

class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self.repository.get_by_id(id=request.id)
       
        if category is None:
            raise CategoryNotFound(f'Category {request.id} Not Found')
        
        return GetCategoryResponse(
            id=category.id, 
            name=category.name, 
            description=category.description, 
            is_active=category.is_active
        ) # dto de resposta

# def create_category(
#         repository: InMemoryCategoryRepository,
#         name: str, 
#         is_active: bool = True, 
#         description: str = ""
# ) -> UUID:
#     try:
#         category = Category(
#             name=name, 
#             description=description, 
#             is_active=is_active
#         )
#     except ValueError as err:
#         raise InvalidCategoryData(err)
    
#     repository.save(category)
#     return category.id