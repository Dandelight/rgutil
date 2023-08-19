from email.mime.text import MIMEText
import smtplib

from attr import dataclass


@dataclass
class MailServer:
    host: str
    port: int


QQMailServer = MailServer("smtp.qq.com", 465)

class Mailer:
    def __init__(self, server: MailServer, dry_run=False) -> None:
        self.smtp = smtplib.SMTP_SSL(server.host, server.port)
        self.dry_run = dry_run

    def login(self, sender, password):
        if not self.dry_run:
            self.smtp.login(sender, password)

    def compose_plain_mail(self, subject, sender, recever, content: str):
        message = MIMEText(content, "plain", "utf-8")
        message["Subject"] = subject
        message["To"] = recever
        message["From"] = sender
        return message

    def send_mail(self, sender, recever, message: MIMEText):
        print(f"From {sender} To {recever} Message{message}")
        if not self.dry_run:
            self.smtp.sendmail(sender, [recever], message.as_string())

    def close(self):
        self.smtp.close()

def test_send_mail():
    subject = "Subject"
    sender = "sender@example.com"
    content = "content"
    recever = "recever@example.com"
    password = "password"

    mailer = Mailer(QQMailServer)
    mailer.login(sender, password)
    message = mailer.compose_plain_mail(subject, sender, recever, content)
    mailer.send_mail(sender, recever, message)
    mailer.close()
