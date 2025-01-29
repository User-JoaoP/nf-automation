import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

def verificar_emails(email_user, email_pass, palavras_chave=["pagamento", "nota fiscal"]):
    # Conecta ao servidor IMAP (ex: Outlook/Hotmail)
    mail = imaplib.IMAP4_SSL("outlook.office365.com")
    mail.login(email_user, email_pass)
    mail.select("inbox")

    # Busca e-mails não lidos
    status, messages = mail.search(None, 'UNSEEN')
    mensagens_relevantes = []

    for num in messages[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Verifica se o corpo contém palavras-chave
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        soup = BeautifulSoup(body, "html.parser")
        texto = soup.get_text().lower()

        if any(palavra in texto for palavra in palavras_chave):
            mensagens_relevantes.append(msg)

    return mensagens_relevantes