import os
import smtplib
from dataclasses import dataclass
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@dataclass
class MailServer:
    host: str
    port: int


QQMailServer = MailServer("smtp.qq.com", 465)

class Mailer:
    def __init__(self, server: MailServer, dry_run=False) -> None:
        self.smtp = smtplib.SMTP_SSL(server.host, server.port)
        self.dry_run = dry_run
        self.smtp.set_debuglevel(1)

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

    def compose_image_mail(
        self,
        subject: str,
        sender: str,
        receivers: list[str],
        content: str,
        attachments: list[str],
        pictures: list[str],
    ):
        """
        :param subject: str,邮件主题
        :param body_content: str,邮件正文
        :param attachs: list,附件地址
        :param pics: list,图片地址
        :return: 发送邮件
        """
        # 构建MIMEMultipart对象代表邮件本身，可以往里面添加文本、图片、附件等
        mm = MIMEMultipart("related")
        mm["From"] = sender
        mm["To"] = ",".join(receivers)
        mm["Subject"] = Header(subject, "utf-8")
        # 2. 添加正文内容
        # 3. 添加附件
        for attach_file in attachments:
            with open(attach_file, "rb") as file_info:
                atta = MIMEText(file_info.read(), "base64", "utf-8")
                atta.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=("utf-8", "", os.path.basename(attach_file)),
                )
                # 添加附件到邮件信息当中去
                mm.attach(atta)
        # 4. 添加图片到附件
        for pic_file in pictures:
            with open(pic_file, "rb") as image:
                image_info = MIMEImage(image.read())
                image_info.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=("utf-8", "", os.path.basename(pic_file)),
                )
                mm.attach(image_info)
        inline_pictures = []
        # 5. 添加图片到正文
        for index, pic_file in enumerate(pictures):
            pic_file_name = os.path.basename(pic_file)
            with open(pic_file, "rb") as image:
                image_info = MIMEImage(image.read())
                image_info.add_header("Content-Id", f"<image{index+1}>")
                mm.attach(image_info)
                inline_pictures.append(
                    f"""<br><img src="cid:image{index+1}" width="300" alt={pic_file_name}></br>"""
                )
        content = content + "".join(inline_pictures)
        mm.attach(MIMEText(content, "html", "utf-8"))
        return mm

    def close(self):
        self.smtp.close()

def test_send_mail():
    subject = "Subject"
    sender = "sender@example.com"
    content = "content"
    recever = "receiver@example.com"
    password = "password"

    mailer = Mailer(QQMailServer)
    mailer.login(sender, password)
    message = mailer.compose_plain_mail(subject, sender, recever, content)
    mailer.send_mail(sender, recever, message)
    mailer.close()


def test_send_image():
    subject = "Subject"
    sender = "sender@example.com"
    password = ""

    content = ""
    receiver = "receiver@example.com"

    mailer = Mailer(QQMailServer)
    mailer.login(sender, password)
    message = mailer.compose_image_mail(
        subject,
        sender,
        [receiver],
        content,
        [],
        ["./yet_another_image.png"],
    )
    mailer.send_mail(sender, receiver, message)
    mailer.close()


if __name__ == "__main__":
    test_send_image()
