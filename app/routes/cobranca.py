from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cobranca import Cobranca
from app.schemas.cobranca import CobrancaCreate
from app.routes.auth import get_current_empresa, get_db
from app.services.plan_service import contar_cobrancas_mes

router = APIRouter(prefix="/cobrancas", tags=["Cobranças"])


@router.post("/")
def criar_cobranca(
    dados: CobrancaCreate,
    db: Session = Depends(get_db),
    empresa = Depends(get_current_empresa)
):

    # 🔒 BLOQUEIO DO PLANO BASIC (limite 50 por mês)
    if empresa.plano == "basic":
        total_mes = contar_cobrancas_mes(db, empresa.id)

        if total_mes >= 50:
            raise HTTPException(
                status_code=403,
                detail="Limite do plano Basic (50 cobranças/mês) atingido. Faça upgrade para o plano Pro."
            )

    # ✅ Se passou da validação, cria normalmente
    nova_cobranca = Cobranca(
        empresa_id=empresa.id,
        cliente_id=dados.cliente_id,
        valor=dados.valor,
        vencimento=dados.vencimento,
        status="pendente"
    )

    db.add(nova_cobranca)
    db.commit()
    db.refresh(nova_cobranca)

    return nova_cobranca
