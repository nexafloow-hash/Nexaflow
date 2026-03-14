# app/routes/risco.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cliente import Cliente
from app.models.cobranca import Cobranca
from app.services.risco import calcular_risco_empresa
from app.auth import get_current_empresa

router = APIRouter(prefix="/dashboard", tags=["Risco"])


@router.get("/risco")
def dashboard_risco(
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_current_empresa)
):

    clientes = db.query(Cliente).filter(
        Cliente.empresa_id == empresa_id
    ).all()

    cobrancas = db.query(Cobranca).filter(
        Cobranca.empresa_id == empresa_id
    ).all()

    resultado = calcular_risco_empresa(clientes, cobrancas)

    return resultado