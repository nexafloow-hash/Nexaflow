from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.cobranca import Cobranca
from app.routes.auth import get_current_empresa, get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def dashboard(db: Session = Depends(get_db), empresa=Depends(get_current_empresa)):
    
    pendentes = db.query(func.count(Cobranca.id)).filter(
        Cobranca.empresa_id == empresa.id,
        Cobranca.status == "pendente"
    ).scalar()

    atrasadas = db.query(func.count(Cobranca.id)).filter(
        Cobranca.empresa_id == empresa.id,
        Cobranca.status == "atrasado"
    ).scalar()

    pagas = db.query(func.count(Cobranca.id)).filter(
        Cobranca.empresa_id == empresa.id,
        Cobranca.status == "pago"
    ).scalar()

    total_em_aberto = db.query(func.sum(Cobranca.valor)).filter(
        Cobranca.empresa_id == empresa.id,
        Cobranca.status.in_(["pendente", "atrasado"])
    ).scalar() or 0

    total_cobrancas = pendentes + atrasadas + pagas

    taxa_inadimplencia = 0
    if total_cobrancas > 0:
        taxa_inadimplencia = (atrasadas / total_cobrancas) * 100

    return {
        "pendentes": pendentes,
        "atrasadas": atrasadas,
        "pagas": pagas,
        "total_em_aberto": float(total_em_aberto),
        "taxa_inadimplencia": round(taxa_inadimplencia, 2)
    }