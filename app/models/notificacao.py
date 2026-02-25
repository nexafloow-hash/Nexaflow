from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, nullable=False)
    cobranca_id = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)  # email / whatsapp
    status = Column(String, nullable=False)  # enviado / erro
    criado_em = Column(DateTime(timezone=True), server_default=func.now())