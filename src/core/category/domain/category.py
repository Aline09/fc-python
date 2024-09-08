from dataclasses import dataclass, field
from uuid import UUID
import uuid
@dataclass
class Category:
    # Tem que declarar o self dentro da função!
    # No python os argumentos obrigatórios vem antes e os opcionais depois
    name: str
    description: str = ""
    is_active: bool = True
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()
    # Não usamos mais essa forma de inicializar abaixo porque estamos usando @dataclass
        
    # def __init__(
    #         self,
    #         name,
    #         id = "", 
    #         description = "", 
    #         is_active = True
    #     ):
    #     self.id = id or uuid.uuid4()
    #     self.name = name
    #     self.description = description
    #     self.is_active = is_active
    
    #     self.validate()
    # Toda a vez que eu tentar exibir um objeto dando um print ao invés de mostrar a classe e a posição de memória ele mostra algo mais semântico ao usuário
    def __str__(self):
        return f"{self.name} - {self.description} - ({self.is_active})"
    
    # Desse modo mesmo que eu não print o valor terei uma forma mais simples de ver os dados 
    def __repr__(self):
        return f"<Category {self.name} ({self.id})>" 
    
    def __eq__(self, other): # a == b -> a.__eq__(b), caso eu tenha 2 categorias com o mesmo id elas são iguais
        if not isinstance(other, Category):
            return False
        
        return self.id == other.id

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name must have less than 255 characteres")
        
        if not self.name: # len(self.name) == 0:
            raise ValueError("Cannot create category with empty name")

    
    def update_category(self, name, description): 
        self.name = name
        self.description = description
        
        self.validate()

    def activate_category(self):
        self.is_active = True
        self.validate()

    def deactivate_category(self):
        self.is_active = False
        self.validate()