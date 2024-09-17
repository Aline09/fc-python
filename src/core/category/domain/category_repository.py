from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list() -> list[Category]:
        raise NotImplementedError