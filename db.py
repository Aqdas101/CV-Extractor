import sqlite3
from typing import List, Tuple

conn = sqlite3.connect('cv_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS cv_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    skills TEXT,                   
                    education TEXT,                
                    past_company_experience INTEGER, 
                    about_section LONGTEXT             
                ) ''')
conn.commit()
conn.close()

def save_cv_into_db(cv_list: list):
    print('Start --- Inserting CV detail in Database')
    cv_list = [str(cv) for cv in cv_list]

    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    query = '''INSERT INTO cv_details (name, email, phone_number, skills, education, past_company_experience, about_section) 
               VALUES (?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(query, cv_list)
    conn.commit()
    conn.close()
    print('End --- Inserting CV detail in Database\n\n')


def get_cv_from_db() -> List[Tuple]:
    print('Start -- Fetch CV details from database...')

    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, email, phone_number, skills, education, past_company_experience, about_section FROM cv_details')
    
    rows = cursor.fetchall()
    
    conn.close()  
    print('End -- Fetch CV details from database\n\n')  
    return rows




# print('This is feteches rows: ', get_cv_from_db())

# info_list = [
#     "John Doe",              # name
#     "john.doe@example.com",  # email
#     "+1234567890",           # phone_number
#     "Python, JavaScript, SQL", # skills
#     "B.Sc. in Computer Science", # education
#     "XYZ Corp, ABC Inc",     # past_company_experience
#     "Passionate software developer with 5+ years of experience in building web applications." # about_section
# ]

    
# save_cv_into_db(info_list)