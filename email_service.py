import smtplib
from email.message import EmailMessage

class Email:
    def __init__(self, reciever: str, email: str, senha: str):
        self.reciever = reciever
        self.sender = email
        self.senha = senha
        self.assunto_email = "A sua noticia resumida :)"
    
    def enviar_email(self, titulo: str, resumo: str) -> None:
        #caso o user queira receber a noticia no email, este codigo envia a noticia
        msg = EmailMessage()
        msg["Subject"] = self.assunto_email
        msg["From"] = self.sender
        msg["To"] = self.reciever
        msg.set_content(f"\t{titulo}\n\n{resumo}\n\n\t\t\tFrom Ai_Noticia team")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.sender, self.senha)
            smtp.send_message(msg)
