from flask import Flask, render_template, request
import os
import openai
import sqlite3
from flask import redirect, url_for, flash
from mail_helper import send_email

from app import get_answer_from_db, get_response_using_openai

app = Flask(__name__)

def get_all_questions():
    conn = sqlite3.connect('interview_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT keyword FROM personal_info UNION SELECT question FROM interview_qa")
    questions = cursor.fetchall()
    
    conn.close()
    return [q[0] for q in questions]

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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
