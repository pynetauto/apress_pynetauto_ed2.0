import smtplib
from email.mime.text import MIMEText

sender_email = "pynetauto1@gmail.com"
recipient_email = "pynetauto@yahoo.com"
subject = "Docker Sendmail Python Email App Test #01"
body = (
    "This is a test email sent using Docker Sendmail Python Email Application utilizing "
    "Gmail's SMTP server with app passwords. You can safely discard this test email. Thank!"
)

msg = MIMEText(body)
msg["From"] = sender_email
msg["To"] = recipient_email
msg["Subject"] = subject

smtp_server = "smtp.gmail.com"
smtp_port = 587

gmail_user = sender_email
gmail_password = "niutfsbjlgjimtdq"

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, recipient_email, msg.as_string())
    print("Email sent using Gmail's SMTP server with app passwords!")
    server.quit()

except Exception as e:
    print(f"Something went wrong: {str(e)}")

print("Your requested task has been completed!")
