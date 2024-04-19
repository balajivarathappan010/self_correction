import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_whom, subject, message):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    sender_email = 'provide_sender_mail'
    sender_password = 'provide_sender_password'
    receiver_email = to_whom
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("email sent successfully")
    except Exception as e:
        print(f'Error:{e}')