import pdfplumber
import spacy
nlp=spacy.load("en_core_web_sm")
SKILLS=[
    "python",
    "django",
    "flask",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "react",
    "react.js",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "machine learning",
    "artificial intelligence",
    "data science",
    "bootstrap",
]

def extract_text_from_pdf(pdf_path):
    text= ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()

            if page_text:
                text += page_text + "\n"
    return text
def extract_skills(text):
    text=text.lower()
    found_skills=[]
    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)
    return list(set(found_skills))

def calculate_resume_score(skills):
    total_skills=len(SKILLS)
    matched_skills=len(skills)
    score=int((matched_skills/total_skills)*100)
    if score > 100:
        score=100
    return score

def calculate_job_match(resume_skills,job_skills):
    """
    Compare resume skills with job skills.
    Return:
        match_percentage
        matched_skills
        missing_skills
    """

    resume_set= {skill.strip().lower() for skill in resume_skills}
    job_set={
        skill.strip().lower()
        for skill in job_skills.split(",")
    }
    matched=list(resume_set & job_set)
    missing=list(job_set - resume_set)
    if len(job_set)==0:
        percentage=0
    else:
        percentage=int(len(matched)/len(job_set)*100)
    return percentage,matched,missing
