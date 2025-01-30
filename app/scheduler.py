import schedule
import time
from app.email_handler import verificar_emails
from app import create_app
from app.email_sender import enviar_cobrancas

def iniciar_agendador():
    with app.app_context():
        schedule.every(1).hours.do(verificar_emails)
        schedule.every().day.at("09:00").do(enviar_cobrancas)  # Envia às 9h
        

app = create_app()

def iniciar_agendador():
    with app.app_context():
        # Verifica e-mails a cada 1 hora
        schedule.every(1).hours.do(verificar_emails)

        while True:
            schedule.run_pending()
            time.sleep(1)

# Inicia em uma thread separada (opcional)
from threading import Thread
Thread(target=iniciar_agendador).start()