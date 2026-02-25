from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.auth import get_current_empresa, get_db
from app.services.plan_service import contar_cobrancas_mes

router = APIRouter(prefix="/plano", tags=["Plano"])


@router.get("/meu-plano")
def meu_plano(
    db: Session = Depends(get_db),
    empresa = Depends(get_current_empresa)
):
    if empresa.plano == "basic":
        limite = 50
    else:
        limite = "ilimitado"

    usado = contar_cobrancas_mes(db, empresa.id)

    restante = None
    if isinstance(limite, int):
        restante = max(limite - usado, 0)

    return {
        "plano": empresa.plano,
        "limite_mensal": limite,
        "usado_este_mes": usado,
        "restante": restante
    }


@router.post("/upgrade")
def upgrade_plano(
    novo_plano: str,
    db: Session = Depends(get_db),
    empresa = Depends(get_current_empresa)
):
    if novo_plano not in ["basic", "pro"]:
        raise HTTPException(status_code=400, detail="Plano inválido.")

    empresa.plano = novo_plano
    db.commit()

    return {"mensagem": f"Plano atualizado para {novo_plano} com sucesso."}