import streamlit as st
import requests


st.set_page_config(
    page_title="Skill Matcher Agent",
    page_icon="🤖"
)


st.title("🤖 Skill Matcher Agent")


# ================= UPLOAD RESUME =================

st.header("📄 Upload Resume")


name = st.text_input(
    "Name"
)

email = st.text_input(
    "Email",
    placeholder="abc@gmail.com"
)


resume_skills = st.text_input(
    "Resume Skills",
    value="python,react,sql,fastapi"
)


resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)



if st.button("⬆️ Upload Resume"):


    if resume is None:

        st.warning(
            "Please upload PDF"
        )


    elif name.strip() == "" or email.strip() == "":

        st.warning(
            "Please fill name and email"
        )


    else:

        try:

            response = requests.post(

                "http://127.0.0.1:8000/upload-resume",

                files={

                    "resume": (
                        resume.name,
                        resume.getvalue(),
                        "application/pdf"
                    )

                },

                data={

                    "name": name.strip(),

                    "email": email.strip(),

                    "skills": resume_skills.strip()

                }
            )


            if response.status_code == 200:

                st.success(
                    "✅ Resume Uploaded Successfully"
                )

            else:

                st.error(
                    "Backend Error"
                )

                st.write(
                    response.text
                )


        except Exception as e:

            st.error(
                "Backend not running"
            )

            st.write(e)




st.divider()



# ================= MATCH =================


st.header("⚡ Match Resume With Job")


job_skills = st.text_input(
    "Job Required Skills",
    value="python,sql,machine learning"
)



if st.button("🔍 Check Match"):


    response = requests.post(

        "http://127.0.0.1:8000/match",

        json={

            "user_skills":

            resume_skills.split(","),


            "required_skills":

            job_skills.split(",")

        }
    )


    result = response.json()



    if "match_score" in result:


        st.success(
            "Match Completed"
        )


        st.metric(
            "Match Score",
            str(result["match_score"]) + "%"
        )


        st.write(
            "✅ Matched Skills:",
            result["matched_skills"]
        )


        st.write(
            "❌ Missing Skills:",
            result["missing_skills"]
        )


    else:

        st.error(result)