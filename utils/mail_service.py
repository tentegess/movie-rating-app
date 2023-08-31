from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

def mail_sender(receiver, subject, content):

    sender = current_app.config["MAIL_USERNAME"]
    port = current_app.config["MAIL_PORT"]
    passwd = current_app.config["MAIL_PASSWORD"]
    host = current_app.config["MAIL_SERVER"]

    msg = MIMEText(content, 'html')

    msg['Subject'] = subject
    msg['From'] = formataddr((str(Header('WatchScore', 'utf-8')), sender))
    msg['To'] = receiver

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(sender, passwd)
        server.sendmail(sender, receiver, msg.as_string())