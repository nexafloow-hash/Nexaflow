from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate
from app.core.deps import get_empresa_atual, get_db

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/")
def criar_cliente(
    cliente: ClienteCreate,
    empresa = Depends(get_empresa_atual),
    db: Session = Depends(get_db)
):
    novo_cliente = Cliente(
        empresa_id=empresa.id,
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


@router.get("/")
def listar_clientes(
    empresa = Depends(get_empresa_atual),
    db: Session = Depends(get_db)
):
    clientes = db.query(Cliente).filter(
        Cliente.empresa_id == empresa.id
    ).all()

    return clientes