# app/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.security import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verify_password(password, user.senha):
        raise HTTPException(status_code=400, detail="Senha incorreta")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}