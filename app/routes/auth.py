from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaLogin
from app.core.security import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    empresa_existente = db.query(Empresa).filter(Empresa.email == empresa.email).first()
    if empresa_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    nova_empresa = Empresa(
        nome=empresa.nome,
        email=empresa.email,
        senha_hash=hash_senha(empresa.senha)
    )

    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return {"message": "Empresa criada com sucesso"}

@router.post("/login")
def login(dados: EmpresaLogin, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.email == dados.email).first()

    if not empresa or not verificar_senha(dados.senha, empresa.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": str(empresa.id)})

    return {"access_token": token, "token_type": "bearer"}


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.security import SECRET_KEY  # se você tiver SECRET_KEY aqui
from app.models.empresa import Empresa

security = HTTPBearer()

def get_current_empresa(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        empresa_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return empresa