import sqlite3


def create_db():

    conn = sqlite3.connect(
        "resumes.db"
    )

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        skills TEXT,
        resume_file TEXT
    )
    """)


    conn.commit()
    conn.close()



create_db()