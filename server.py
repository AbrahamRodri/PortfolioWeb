from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import sqlite3
import smtplib
from quickstart import main , add_event_to_calendar  # Assuming this is the function to fetch events
from app import get_answer_from_db, get_response_using_openai  # Assuming these are functions for processing questions
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = os.urandom(24)

def round_time_to_nearest(time_str):
    """Round the time string to the nearest hour or half-hour."""
    time = datetime.strptime(time_str, '%H:%M')
    rounded_minute = (time.minute // 30) * 30  # Round to the nearest half-hour
    if rounded_minute == 60:
        rounded_minute = 0
        time += timedelta(hours=1)
    rounded_time = time.replace(minute=rounded_minute, second=0, microsecond=0)
    return rounded_time.strftime('%H:%M')

def get_all_questions():
    conn = sqlite3.connect('interview_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT keyword FROM personal_info UNION SELECT question FROM interview_qa")
    questions = cursor.fetchall()

    conn.close()
    return [q[0] for q in questions]

def create_calendar_service():
    # Path to the service account key file
    SERVICE_ACCOUNT_FILE = '/home/rodriguezabrahamdev/service_account.json'

    # Scopes required for the calendar access
    # Scopes required for the calendar access
    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


    # Authenticate and create a service object
    credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    return service

def send_email_and_create_event(name, email, phone, date, time, message):
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

    # Round the time to the nearest hour or half-hour
    rounded_time = round_time_to_nearest(time)

    # Create event in Google Calendar
    event_summary = 'New Contact Form Submission'
    event_description = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nPreferred Date: {date}\nPreferred Time: {rounded_time}\nMessage: {message}"
    start_datetime = datetime.strptime(f"{date} {rounded_time}", '%Y-%m-%d %H:%M')
    end_datetime = start_datetime + timedelta(hours=1)  # Assuming events are one hour long

    event_id = add_event_to_calendar(event_summary, start_datetime, end_datetime, event_description)
    if event_id:
        print("Event created successfully with ID:", event_id)
    else:
        print("Failed to create event.")

    return event_id


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/get-events')
def get_events():
    events = main()  # Assuming this function fetches events
    return jsonify(events)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get the form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    date = request.form.get('date')
    time = request.form.get('time')
    message = request.form.get('message')

    # Send the email and create an event
    send_email_and_create_event(name, email, phone, date, time, message)


    # Flash a success message or handle as necessary
    flash('Thank you for your message. We will be in touch soon!')

    # Redirect back to the contact page or a 'thank you' page
    return redirect(url_for('calendar'))

@app.route('/project', methods=['GET', 'POST'])
def project():
    question = ""
    answer = ""
    questions = get_all_questions()

    if request.method == 'POST':
        user_query = request.form.get('question')

        conn = sqlite3.connect('interview_data.db')
        cursor = conn.cursor()

        context = get_answer_from_db(user_query, cursor)
        answer = get_response_using_openai(user_query, context)

        question = user_query
        conn.close()

    return render_template('projects.html', question=question, answer=answer, questions=questions)

@app.route('/approve')
def approve_appointment():
    # Logic to approve the appointment
    # You can access request parameters like name and email using request.args.get('parameter_name')
    name = request.args.get('name')
    email = request.args.get('email')
    # Update the status of the appointment in your database, or perform any other actions
    return "Appointment approved successfully."

@app.route('/deny')
def deny_appointment():
    # Logic to deny the appointment
    # You can access request parameters like name and email using request.args.get('parameter_name')
    name = request.args.get('name')
    email = request.args.get('email')
    # Update the status of the appointment in your database, or perform any other actions
    return "Appointment denied."

if __name__ == '__main__':
    app.run(debug=True)