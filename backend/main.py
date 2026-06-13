from fastapi import FastAPI, UploadFile, File, Form
from backend.matcher import match_skills
import shutil
import sqlite3
import os


app = FastAPI()


# ================= PATH =================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATABASE_FOLDER = os.path.join(
    BASE_DIR,
    "database"
)

os.makedirs(
    DATABASE_FOLDER,
    exist_ok=True
)


DB_PATH = os.path.join(
    DATABASE_FOLDER,
    "resumes.db"
)



# ================= HOME =================

@app.get("/")
def home():
    return {
        "message": "Skill Matcher API Running"
    }



# ================= MATCH =================

@app.post("/match")
def skill_match(data: dict):

    result = match_skills(
        data["user_skills"],
        data["required_skills"]
    )

    return result




# ================= UPLOAD RESUME =================

@app.post("/upload-resume")
async def upload_resume(
    name: str = Form(...),
    email: str = Form(...),
    skills: str = Form(...),
    resume: UploadFile = File(...)
):

    # uploads folder

    upload_dir = os.path.join(
        BASE_DIR,
        "uploads"
    )


    os.makedirs(
        upload_dir,
        exist_ok=True
    )


    file_path = os.path.join(
        upload_dir,
        resume.filename
    )



    # save pdf

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )



    # database

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()



    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS resumes
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            skills TEXT,
            resume_file TEXT
        )
        """
    )



    cursor.execute(
        """
        INSERT INTO resumes
        (
            name,
            email,
            skills,
            resume_file
        )

        VALUES (?,?,?,?)
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