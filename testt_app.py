import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# -----------------------------------
# Configuration (Ganti dengan API sebenar anda)
# -----------------------------------
ADZUNA_APP_ID = 'f8ccd3fb'       # Gantikan dengan App ID sebenar
ADZUNA_APP_KEY = '98e52090fbfa37dfeec774ab8bf8aeec'  # Gantikan dengan App Key sebenar

# -----------------------------------
# Helper Functions
# -----------------------------------

def fetch_jobs(role, location, results_per_page=20):
    # Gunakan endpoint UK (gb)
    url = 'https://api.adzuna.com/v1/api/jobs/gb/search/1'
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page': results_per_page,
        'what': role,
        'where': location,
        'content-type': 'application/json'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('results', [])
    elif response.status_code == 401:
        st.error("Akses tidak dibenarkan: Sila semak kelayakan API anda (App ID dan App Key).")
        return []
    else:
        st.error(f"Ralat mendapatkan kerja: {response.status_code} - {response.reason}")
        return []

def extract_skills(job_descriptions, top_n=10):
    sample_skills = [
        'python', 'java', 'sql', 'excel', 'communication', 'teamwork',
        'project management', 'data analysis', 'machine learning', 'aws',
        'javascript', 'c++', 'linux', 'git', 'docker'
    ]
    skill_counts = Counter()
    for desc in job_descriptions:
        desc_lower = desc.lower()
        for skill in sample_skills:
            if skill in desc_lower:
                skill_counts[skill] += 1
    return skill_counts.most_common(top_n)

def recommend_courses(skills):
    course_catalog = {
        'python': [{'title': 'Python for Everybody', 'url': 'https://www.coursera.org/specializations/python'}],
        'java': [{'title': 'Java Programming', 'url': 'https://www.coursera.org/specializations/java-programming'}],
        'sql': [{'title': 'SQL for Data Science', 'url': 'https://www.coursera.org/learn/sql-for-data-science'}],
        'excel': [{'title': 'Excel for Business', 'url': 'https://www.coursera.org/specializations/excel'}],
        'communication': [{'title': 'Communication Skills', 'url': 'https://www.coursera.org/learn/wharton-communication-skills'}],
        'teamwork': [{'title': 'Teamwork Skills', 'url': 'https://www.coursera.org/learn/teamwork-skills'}],
        'project management': [{'title': 'Project Management', 'url': 'https://www.coursera.org/learn/project-management-principles'}],
        'data analysis': [{'title': 'Data Analysis with Python', 'url': 'https://www.coursera.org/learn/data-analysis-with-python'}],
        'machine learning': [{'title': 'Machine Learning', 'url': 'https://www.coursera.org/learn/machine-learning'}],
        'aws': [{'title': 'AWS Fundamentals', 'url': 'https://www.coursera.org/specializations/aws-fundamentals'}],
        'javascript': [{'title': 'Intro to JavaScript', 'url': 'https://www.codecademy.com/learn/introduction-to-javascript'}],
        'c++': [{'title': 'C++ Basics', 'url': 'https://www.udemy.com/course/beginning-c-plus-plus-programming/'}],
        'linux': [{'title': 'Intro to Linux', 'url': 'https://www.edx.org/course/introduction-to-linux'}],
        'git': [{'title': 'Version Control with Git', 'url': 'https://www.coursera.org/learn/version-control-with-git'}],
        'docker': [{'title': 'Docker for Beginners', 'url': 'https://www.coursera.org/learn/docker'}]
    }
    recommendations = {}
    for skill, _ in skills:
        if skill in course_catalog:
            recommendations[skill] = course_catalog[skill]
    return recommendations

# -----------------------------------
# Streamlit App
# -----------------------------------

def main():
    st.set_page_config(layout="wide")
    st.title("📊 SkillMap AI")
    st.markdown("*Personalized learning based on job market demand.*")

    # Input untuk job role dan lokasi UK
    role = st.text_input("🎯 Enter Job Role:", "Data Analyst")
    location = st.text_input("📍 Enter Location:", "London")

    if st.button("🔍 Analyze Skills"):
        jobs = fetch_jobs(role, location)

        if not jobs:
            st.warning("Tiada data kerja dijumpai. Sila cuba kerja atau lokasi yang lain.")
            return

        st.success(f"✅ Jumpa {len(jobs)} senarai kerja")

        job_descriptions = [job.get('description', '') for job in jobs]
        skills = extract_skills(job_descriptions)

        # Papar table skill
        st.subheader("📈 Top Skills Extracted")
        skills_df = pd.DataFrame(skills, columns=["Skill", "Frequency"])
        st.dataframe(skills_df)

        # Papar contoh senarai kerja
        st.subheader("💼 Sample Job Listings")
        job_preview = pd.DataFrame([
            {"Title": job.get("title"), "Company": job.get("company", {}).get("display_name", "N/A")}
            for job in jobs[:10]
        ])
        st.table(job_preview)

        # Carta bar frequency skill
        st.subheader("📊 Skill Frequency Bar Chart")
        fig1, ax1 = plt.subplots()
        ax1.barh(skills_df["Skill"], skills_df["Frequency"], color='lightgreen')
        ax1.set_xlabel("Frequency")
        ax1.set_ylabel("Skill")
        st.pyplot(fig1)

        # Carta pai share skill
        st.subheader("🧁 Skill Share Pie Chart")
        fig2, ax2 = plt.subplots()
        ax2.pie(skills_df["Frequency"], labels=skills_df["Skill"], autopct='%1.1f%%', startangle=140)
        ax2.axis('equal')
        st.pyplot(fig2)

        # Cadangan kursus
        st.subheader("🎓 Recommended Courses")
        course_recs = recommend_courses(skills)
        for skill, courses in course_recs.items():
            st.markdown(f"*{skill.capitalize()}*")
            for course in courses:
                st.markdown(f"🔗 [{course['title']}]({course['url']})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

