import smtplib
from server.py import create_calendar_service
import datetime
from email.mime.text import MIMEText

def send_email_and_create_event(name, email, message):
    # Gmail credentials
    from_email = "rodriguez.abraham6369@gmail.com"  # Replace with your actual email
    app_password = "gujf xzhi wnoy awdk"

    # Email details
    to_email = "rodriguez.abraham63@outlook.com"
    subject = "New contact form submission"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    # Construct email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(from_email, app_password)
        smtp_server.send_message(msg)

    # Create event in Google Calendar
    calendar_service = create_calendar_service()  # Create Google Calendar service
    event = {
        'summary': 'New Contact Form Submission',
        'description': f"Name: {name}\nEmail: {email}\nMessage: {message}",
        'start': {
            'dateTime': datetime.datetime.now().isoformat(),
            'timeZone': 'Your timezone',
        },
        'end': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'Your timezone',
        },
    }
    event = calendar_service.events().insert(calendarId='primary', body=event).execute()
    return event