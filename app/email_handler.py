import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from datetime import datetime
from app import app, db
from app.models import Fornecedor

def verificar_emails():
    # Configurações de e-mail (substitua com suas credenciais)
    EMAIL_USER = "tifinan@hpeautos.com.br"
    EMAIL_PASSWORD = "sua_senha"
    IMAP_SERVER = "outlook.office365.com"  # Ou servidor do seu provedor

    try:
        # Conecta ao servidor IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        mail.select("inbox")

        # Busca e-mails não lidos com palavras-chave
        status, messages = mail.search(None, 'UNSEEN', '(OR SUBJECT "nota fiscal" BODY "pagamento")')
        messages = messages[0].split()

        for msg_id in messages:
            _, msg_data = mail.fetch(msg_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extrai dados do e-mail
            sender = msg.get("From")
            subject = decode_header(msg.get("Subject"))[0][0]
            body = ""
            anexos = []

            # Processa o corpo e anexos
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                    elif "attachment" in part.get("Content-Disposition", ""):
                        filename = part.get_filename()
                        if filename:
                            anexos.append(filename)
            else:
                body = msg.get_payload(decode=True).decode()

            # Verifica se há anexos ou links relevantes
            if anexos or "pagamento" in body.lower():
                # Atualiza o status do fornecedor (exemplo básico)
                fornecedor = Fornecedor.query.filter_by(email=sender).first()
                if fornecedor:
                    fornecedor.status = "enviado"
                    db.session.commit()

        mail.close()
        mail.logout()
        return True

    except Exception as e:
        app.logger.error(f"Erro ao verificar e-mails: {str(e)}")
        return False