from pydantic import BaseModel
from datetime import datetime

class CobrancaCreate(BaseModel):
    cliente_id: int
    valor: float
    vencimento: datetime