import sqlite3

def insert_into_personal_info(keyword, answer):
    conn = sqlite3.connect('interview_data.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO personal_info (keyword, answer) VALUES (?, ?)", (keyword, answer))
    
    conn.commit()
    conn.close()

def insert_into_interview_qa(question, answer):
    conn = sqlite3.connect('interview_data.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO interview_qa (question, answer) VALUES (?, ?)", (question, answer))
    
    conn.commit()
    conn.close()


def print_all_data_from_table(table_name):
    conn = sqlite3.connect('interview_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM {}".format(table_name))
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
        
    conn.close()

insert_into_personal_info("Where is Abraham from?", "The context is that abraham, who you are an assistant answering questions for, lives in fresno california." )



# Example usage:
print_all_data_from_table('personal_info')
print_all_data_from_table('interview_qa')
