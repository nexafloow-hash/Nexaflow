from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.empresa import Empresa
from app.dependencies import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/empresas", tags=["Empresas"])


@router.get("/")
def listar_empresas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    empresas = db.query(Empresa).all()
    return empresas