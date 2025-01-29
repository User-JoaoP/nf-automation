import schedule
import time
from threading import Thread
from app.email_handler import verificar_emails
from app.models import Fornecedor, db

def iniciar_agendador():
    def tarefa_verificar_emails():
        with app.app_context():
            # Exemplo: verifica e-mails a cada 1 hora
            emails = verificar_emails("tifinan@hpeautos.com.br", "SUA_SENHA")
            # Lógica para registrar no banco de dados

    def tarefa_enviar_cobrancas():
        with app.app_context():
            # Exemplo: verifica prazos diariamente às 8h
            fornecedores_pendentes = Fornecedor.query.filter_by(status='pendente').all()
            for fornecedor in fornecedores_pendentes:
                # Lógica para enviar e-mail de cobrança
                pass

    schedule.every().hour.do(tarefa_verificar_emails)
    schedule.every().day.at("08:00").do(tarefa_enviar_cobrancas)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Inicia o agendador em uma thread separada
Thread(target=iniciar_agendador).start()