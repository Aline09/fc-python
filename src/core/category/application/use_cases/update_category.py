
from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.application.use_cases.category_repository import CategoryRepository

@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None

class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        # Category Existe?
        category = self.repository.get_by_id(request.id)
        try:
            if category is None:
                raise CategoryNotFound(f'Category {request.id} Not Found')

            current_name = category.name
            current_description = category.description

            if request.name is not None:
                current_name = request.name
            
            if request.description is not None:
                current_description = request.description

            if request.is_active is True:
                category.activate_category()

            if request.is_active is False:
                category.deactivate_category()
            
            category.update_category(current_name, current_description)
        except ValueError as error:
            raise InvalidCategoryData(error)

        self.repository.update(category)