from flask import Flask, render_template, request , jsonify
import os
import openai
import sqlite3
from flask import redirect, url_for, flash
from mail_helper import send_email

from quickstart import main

from app import get_answer_from_db, get_response_using_openai

app = Flask(__name__)

app.secret_key = os.urandom(24)

def get_all_questions():
    conn = sqlite3.connect('interview_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT keyword FROM personal_info UNION SELECT question FROM interview_qa")
    questions = cursor.fetchall()

    conn.close()
    return [q[0] for q in questions]


@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get the form data
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Send the email
    send_email(name, email, message)

    # Flash a success message or handle as necessary
    flash('Thank you for your message. We will be in touch soon!')

    # Redirect back to the contact page or a 'thank you' page
    return redirect(url_for('contact'))

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



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calendar')
def contact():
    return render_template('calendar.html')

@app.route('/get-events')
def get_events():

    events = main()


    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
