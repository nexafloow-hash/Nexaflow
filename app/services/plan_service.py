from sqlalchemy.orm import Session
from sqlalchemy import extract
from datetime import datetime
from app.models.cobranca import Cobranca

def contar_cobrancas_mes(db: Session, empresa_id: int):
    now = datetime.utcnow()

    total = db.query(Cobranca).filter(
        Cobranca.empresa_id == empresa_id,
        extract("month", Cobranca.created_at) == now.month,
        extract("year", Cobranca.created_at) == now.year
    ).count()

    return total