# mail_helper.py

import smtplib
from email.mime.text import MIMEText

def send_email(name, email, message):
    from_email = "rodriguez.abraham6369@gmail.com"  # Replace with your actual email
    app_password = "wuas ctsy jdfk duxr"

    to_email = "rodriguez.abraham63@outlook.com"
    subject = "New contact form submission"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(from_email, app_password)
        smtp_server.send_message(msg)