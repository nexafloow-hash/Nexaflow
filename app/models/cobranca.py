from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Cobranca(Base):
    __tablename__ = "cobrancas"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    valor = Column(Float, nullable=False)
    vencimento = Column(DateTime, nullable=False)

    status = Column(String, default="pendente")
    lembrete_enviado = Column(Boolean, default=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())