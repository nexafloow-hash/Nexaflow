from fastapi import APIRouter
from app.services.whatsapp_service import enviar_whatsapp

router = APIRouter(prefix="/teste", tags=["Teste"])

@router.post("/whatsapp")
def teste_whatsapp(numero: str, mensagem: str):
    return enviar_whatsapp(numero, mensagem)