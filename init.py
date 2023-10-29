import sqlite3

def setup_database():
    conn = sqlite3.connect('interview_data.db')
    cursor = conn.cursor()

    # Create the personal_info table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personal_info (
        id INTEGER PRIMARY KEY,
        keyword TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    ''')

    # Create the interview_qa table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interview_qa (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

setup_database()
