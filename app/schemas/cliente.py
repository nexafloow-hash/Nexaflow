from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr | None = None
    telefone: str | None = None