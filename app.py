import os
import openai
import sqlite3

def get_answer_from_db(query, cursor):
    # Try to get answer from personal_info
    cursor.execute("SELECT answer FROM personal_info WHERE keyword=?", (query,))
    result = cursor.fetchone()
    if result:
        print(f"From DB: {result[0]}")
        return result[0]

    # Try to get answer from interview_qa
    cursor.execute("SELECT answer FROM interview_qa WHERE question=?", (query,))
    result = cursor.fetchone()
    if result:
        return result[0]

    return None

API_KEY = open("API_KEY", "r").read().strip()
openai.api_key = API_KEY

def get_response_using_openai(query, context=None):
    API_KEY = open("API_KEY", "r").read().strip()
    openai.api_key = API_KEY

    messages = [
        {"role": "system", "content": "You are an assistant with knowledge about Abraham's personal information. Answer questions using this context and improve on the context for an interesting interview response."},
        {"role": "user", "content": query}
    ]
    if context:
        messages.append({"role": "assistant", "content": context})
        print(f"Messages to OpenAI: {messages}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
    )

    return response.choices[0].message['content'].strip()
