import smtplib
from email.mime.text import MIMEText

def send_email():
    sender_email = "pynetauto1@gmail.com"
    recipient_email = "pynetauto@yahoo.com"
    subject = "SW1 is not reachable for more than 60 seconds!"
    body = ("SW1 is not reachable. Please investigate. Thanks!" )

    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    gmail_user = sender_email
    gmail_password = "niutfsbjlgjimtdq"  # Replace with your app password

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            print("Failure notification email sent by Docker Sendmail!")
    except Exception as e:
        print(f"Something went wrong: {str(e)}")

