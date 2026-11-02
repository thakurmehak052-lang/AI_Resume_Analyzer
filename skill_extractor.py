
import re

SKILLS = [
    "Python", "Java", "C++", "C", "SQL",
    "HTML", "CSS", "JavaScript", "React",
    "Node.js", "Django", "Flask",
    "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "NLP",
    "Data Analysis", "Data Visualization",
    "Power BI", "Tableau", "Excel",
    "Pandas", "NumPy", "Scikit-learn",
    "TensorFlow", "Git", "GitHub",
    "MySQL", "MongoDB", "PostgreSQL",
    "AWS", "Azure", "Docker",
    "Communication", "Problem Solving",
    "Leadership", "Teamwork"
]


def extract_skills(text):
    found_skills = []
    text = text.lower()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills
