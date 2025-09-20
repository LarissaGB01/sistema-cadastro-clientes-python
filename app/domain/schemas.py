from pydantic import BaseModel

class ClienteDTO(BaseModel):
    cpf: str
    nome: str