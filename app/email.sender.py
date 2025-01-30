import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from app import app, db
from app.models import Fornecedor

def enviar_cobrancas():
    fornecedores_pendentes = Fornecedor.query.filter(
        Fornecedor.prazo < datetime.now().date(),
        Fornecedor.status == "pendente"
    ).all()

    for fornecedor in fornecedores_pendentes:
        mensagem = f"""
        Prezado {fornecedor.nome},
        
        Verificamos que a nota fiscal referente ao período ainda não foi enviada.
        Por favor, regularize a situação o mais breve possível.
        
        Atenciosamente,
        Equipe Financeira
        """

        msg = MIMEText(mensagem)
        msg["Subject"] = "Lembrete de Envio de Nota Fiscal"
        msg["From"] = "tifinan@hpeautos.com.br"
        msg["To"] = fornecedor.email

        try:
            with smtplib.SMTP("smtp.office365.com", 587) as server:  # Configurações do Outlook
                server.starttls()
                server.login("tifinan@hpeautos.com.br", "sua_senha")
                server.send_message(msg)
                app.logger.info(f"Cobrança enviada para {fornecedor.email}")
        except Exception as e:
            app.logger.error(f"Erro ao enviar e-mail: {str(e)}")