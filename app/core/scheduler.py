from apscheduler.schedulers.background import BackgroundScheduler
from app.services.automacao import verificar_cobrancas

scheduler = BackgroundScheduler()

def iniciar_scheduler():
    scheduler.add_job(
        verificar_cobrancas,
        "interval",
        minutes=1
    )
    scheduler.start()