from fastapi import FastAPI
from app.database import engine, Base
from app.models import empresa, cliente, cobranca
from app.routes import auth
from app.routes import clientes
from app.routes import cobranca
from app.core.scheduler import iniciar_scheduler
from app.models import notificacao
from app.routes import teste_whatsapp
from app.routes import dashboard
from app.routes import plano


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

app.include_router(clientes.router)

app.include_router(cobranca.router)

app.include_router(teste_whatsapp.router)

app.include_router(dashboard.router)

app.include_router(plano.router)

@app.on_event("startup")
def startup_event():
    iniciar_scheduler()

@app.get("/")
def root():
    return {"message": "Sistema de Cobrança SaaS rodando 🚀"}