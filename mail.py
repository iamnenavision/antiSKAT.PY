import smtplib
from email.mime.text import MIMEText

def send_message(message):
    sender = "mrneltapi@gmail.com"
    password = "010999aaa"
    receiver = "61pav03@mail.ru"
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["subject"] = "ExamBot log"
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        return "😉 Письмо отправлено разработчику!"
    except Exception as e:
        return f"{e}\n😢 Письмо не отправлено "

