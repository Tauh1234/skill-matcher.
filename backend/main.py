from fastapi import FastAPI, UploadFile, File, Form
import sqlite3
import os
from matcher import match_skills


app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


DB_PATH = os.path.join(
    BASE_DIR,
    "resumes.db"
)



def create_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT,

        skills TEXT,

        resume_path TEXT

    )
    """)


    conn.commit()
    conn.close()



create_db()



@app.get("/")
def home():

    return {
        "message": "Skill Matcher API Running"
    }



@app.post("/upload-resume")
async def upload_resume(

    name: str = Form(...),

    email: str = Form(...),

    skills: str = Form(...),

    resume: UploadFile = File(...)

):


    file_path = os.path.join(
        UPLOAD_DIR,
        resume.filename
    )


    with open(file_path, "wb") as f:

        f.write(
            await resume.read()
        )



    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()



    cursor.execute(

        """
        INSERT INTO resumes
        (name,email,skills,resume_path)

        VALUES(?,?,?,?)
        """,

        (
            name,
            email,
            skills,
            file_path
        )

    )


    conn.commit()
    conn.close()



    return {

        "message":
        "Resume uploaded successfully"

    }





@app.post("/match")
def match(data: dict):


    user_skills = data["user_skills"]

    required_skills = data["required_skills"]



    result = match_skills(

        user_skills,

        required_skills

    )


    return result