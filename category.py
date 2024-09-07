import uuid
class Category:
    # Tem que declarar o self dentro da função!
    # No python os argumentos obrigatórios vem antes e os opcionais depois
    def __init__(
            self,
            name,
            id = "", 
            description = "", 
            is_active = True
        ):
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active
    
        if len(self.name) > 255:
            raise ValueError("name must have less than 256 characteres")
    # Toda a vez que eu tentar exibir um objeto dando um print ao invés de mostrar a classe e a posição de memória ele mostra algo mais semântico ao usuário
    def __str__(self):
        return f"{self.name} - {self.description} - ({self.is_active})"
    
    # Desse modo mesmo que eu não print o valor terei uma forma mais simples de ver os dados 
    def __repr__(self):
        return f"<Category {self.name} ({self.id})>" 
    
    def update_category(self, name, description): 
        self.name = name
        self.description = description
        
        if len(self.name) > 255:
            raise ValueError("name must have less than 256 characteres")
