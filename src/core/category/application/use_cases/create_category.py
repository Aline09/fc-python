from dataclasses import dataclass
from uuid import UUID

# Application depende de domain
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
# from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository - não importamos mais de um módulo de nível mais baixo
from src.core.category.domain.category import Category

@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True

@dataclass
class CreateCategoryResponse:
    id: UUID

class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository
    
    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            category = Category(
                name=request.name, 
                description=request.description, 
                is_active=request.is_active
            )
        except ValueError as err:
            raise InvalidCategoryData(err)
        
        self.repository.save(category)
        return CreateCategoryResponse(id=category.id) # dto de resposta

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