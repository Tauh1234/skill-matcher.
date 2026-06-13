from backend.skills import SKILLS


def match_skills(user_skills, required_skills):

    user_skills = [
        skill.lower()
        for skill in user_skills
    ]

    required_skills = [
        skill.lower()
        for skill in required_skills
    ]


    matched = []
    missing = []


    for skill in required_skills:

        if skill in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)


    score = 0

    if len(required_skills) > 0:
        score = int(
            (len(matched) / len(required_skills)) * 100
        )


    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }