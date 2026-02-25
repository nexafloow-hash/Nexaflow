from pydantic import BaseModel, EmailStr, Field

class EmpresaCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)

class EmpresaLogin(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)