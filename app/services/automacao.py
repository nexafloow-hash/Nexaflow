from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.cobranca import Cobranca
from app.models.cliente import Cliente
from app.models.empresa import Empresa
from app.models.notificacao import Notificacao
from app.services.email_service import enviar_email
from app.services.whatsapp_service import enviar_whatsapp


def verificar_cobrancas():
    db: Session = SessionLocal()

    try:
        agora = datetime.utcnow()

        cobrancas = db.query(Cobranca).filter(
            Cobranca.status == "pendente",
            Cobranca.lembrete_enviado == False
        ).all()

        for cobranca in cobrancas:
            cliente = db.query(Cliente).filter(
                Cliente.id == cobranca.cliente_id
            ).first()

            empresa = db.query(Empresa).filter(
                Empresa.id == cobranca.empresa_id
            ).first()

            if not cliente or not empresa:
                continue

            mensagem = None

            if cobranca.vencimento.date() == (agora.date() + timedelta(days=1)):
                mensagem = f"Olá {cliente.nome}, sua cobrança de R$ {cobranca.valor} vence amanhã."

            elif cobranca.vencimento < agora:
                cobranca.status = "atrasado"
                mensagem = f"Olá {cliente.nome}, sua cobrança de R$ {cobranca.valor} está em atraso."

            if not mensagem:
                continue

            # EMAIL
            if cliente.email:
                try:
                    enviar_email(cliente.email, "Cobrança", mensagem)

                    db.add(Notificacao(
                        empresa_id=empresa.id,
                        cobranca_id=cobranca.id,
                        tipo="email",
                        status="enviado"
                    ))

                except:
                    db.add(Notificacao(
                        empresa_id=empresa.id,
                        cobranca_id=cobranca.id,
                        tipo="email",
                        status="erro"
                    ))

            # WHATSAPP (somente plano pro)
            if empresa.plano == "pro" and cliente.telefone:
                try:
                    enviar_whatsapp(cliente.telefone, mensagem)

                    db.add(Notificacao(
                        empresa_id=empresa.id,
                        cobranca_id=cobranca.id,
                        tipo="whatsapp",
                        status="enviado"
                    ))

                except:
                    db.add(Notificacao(
                        empresa_id=empresa.id,
                        cobranca_id=cobranca.id,
                        tipo="whatsapp",
                        status="erro"
                    ))

            cobranca.lembrete_enviado = True

        db.commit()

    finally:
        db.close()