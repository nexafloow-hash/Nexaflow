from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.auth import get_current_empresa
from app.models import Cliente, Cobranca
import csv
import io

router = APIRouter(prefix="/importacao", tags=["Importação"])

@router.post("/csv")
async def importar_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    empresa=Depends(get_current_empresa)
):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    for row in reader:
        nome = row["nome_cliente"]
        email = row.get("email")
        telefone = row.get("telefone")
        valor = float(row["valor"])
        vencimento = row["vencimento"]
        status = row.get("status", "pendente")

        # Verifica se cliente já existe
        cliente = db.query(Cliente).filter(
            Cliente.nome == nome,
            Cliente.empresa_id == empresa.id
        ).first()

        if not cliente:
            cliente = Cliente(
                nome=nome,
                email=email,
                telefone=telefone,
                empresa_id=empresa.id
            )
            db.add(cliente)
            db.commit()
            db.refresh(cliente)

        cobranca = Cobranca(
            empresa_id=empresa.id,
            cliente_id=cliente.id,
            valor=valor,
            vencimento=vencimento,
            status=status
        )

        db.add(cobranca)

    db.commit()

    return {"message": "Importação realizada com sucesso!"}