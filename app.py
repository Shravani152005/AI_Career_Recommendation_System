
from flask import Flask, render_template, request
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


# Database connection
def get_db_connection():
    conn = sqlite3.connect("careerai.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database tables
def create_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            education TEXT,
            skills TEXT,
            interest TEXT,
            domain TEXT,
            experience TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS recommendation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            career_name TEXT,
            score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profiles(id)
        )
    """)

    conn.commit()
    conn.close()


create_database()


# Career profiles
careers = [
    {
        "name": "Software Developer",
        "interest": "Programming",
        "domain": "Software Development",
        "skills": ["python", "java", "javascript", "git"],
        "description": "Develop software applications, solve programming problems and build computer systems."
    },
    {
        "name": "AI / Machine Learning Engineer",
        "interest": "Artificial Intelligence",
        "domain": "AI and Machine Learning",
        "skills": ["python", "machine learning", "sql", "statistics"],
        "description": "Build artificial intelligence applications, machine learning models and intelligent systems."
    },
    {
        "name": "Data Scientist",
        "interest": "Data Analysis",
        "domain": "Data Science",
        "skills": ["python", "sql", "pandas", "statistics"],
        "description": "Analyze data, discover patterns, create visualizations and develop data-driven solutions."
    },
    {
        "name": "Web Developer",
        "interest": "Web Development",
        "domain": "Web Development",
        "skills": ["html", "css", "javascript", "react"],
        "description": "Design and develop websites, frontend interfaces and web applications."
    },
    {
        "name": "Cybersecurity Analyst",
        "interest": "Cyber Security",
        "domain": "Cyber Security",
        "skills": ["networking", "python", "linux", "security"],
        "description": "Protect computer systems, identify security threats and prevent cyber attacks."
    },
    {
        "name": "DevOps Engineer",
        "interest": "Software Development",
        "domain": "DevOps",
        "skills": ["linux", "docker", "git", "python", "cloud"],
        "description": "Automate software development processes, manage deployment pipelines and maintain applications."
    },
    {
        "name": "Cloud Engineer",
        "interest": "Cloud Computing",
        "domain": "Cloud Computing",
        "skills": ["aws", "azure", "linux", "networking", "python"],
        "description": "Design, deploy and manage cloud infrastructure and cloud-based applications."
    },
    {
        "name": "UI/UX Designer",
        "interest": "Design",
        "domain": "UI and UX Design",
        "skills": ["figma", "html", "css", "wireframing", "prototyping"],
        "description": "Create user-friendly interfaces, design layouts and improve digital user experiences."
    },
    {
        "name": "Mobile App Developer",
        "interest": "App Development",
        "domain": "Mobile Development",
        "skills": ["java", "kotlin", "flutter", "dart", "javascript"],
        "description": "Develop mobile applications for Android and iOS platforms."
    },
    {
        "name": "Database Administrator",
        "interest": "Data Management",
        "domain": "Database Management",
        "skills": ["sql", "mysql", "oracle", "database", "python"],
        "description": "Manage databases, maintain data security and optimize database performance."
    }
]


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Assessment page
@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


# Recommendation history page
@app.route("/history")
def history():

    conn = get_db_connection()

    history_data = conn.execute("""
        SELECT
            student_profiles.id,
            student_profiles.name,
            student_profiles.education,
            student_profiles.skills,
            student_profiles.interest,
            student_profiles.domain,
            student_profiles.experience,
            student_profiles.created_at,
            recommendation_results.career_name,
            recommendation_results.score,
            recommendation_results.matched_skills,
            recommendation_results.missing_skills
        FROM student_profiles
        LEFT JOIN recommendation_results
        ON student_profiles.id = recommendation_results.student_id
        ORDER BY student_profiles.id DESC,
                 recommendation_results.score DESC
    """).fetchall()

    conn.close()

    return render_template(
        "history.html",
        history_data=history_data
    )


# Career details page
@app.route("/career/<career_name>")
def career_details(career_name):

    selected_career = None

    for career in careers:
        if career["name"] == career_name:
            selected_career = career
            break

    if selected_career is None:
        return "Career not found", 404

    return render_template(
        "career.html",
        career=selected_career
    )


# Career recommendation
@app.route("/recommend", methods=["POST"])
def recommend():

    # Get assessment details
    name = request.form.get("name", "").strip()
    education = request.form.get("education", "").strip()
    skills_input = request.form.get("skills", "").strip()
    interest = request.form.get("interest", "").strip()
    domain = request.form.get("domain", "").strip()
    experience = request.form.get("experience", "").strip()

    # Validate assessment details
    if not all([name, education, skills_input, interest, domain, experience]):
        return "Please complete all assessment fields before submitting.", 400

    # Clean student skills
    skills = [
        skill.strip().lower()
        for skill in skills_input.split(",")
        if skill.strip()
    ]

    if not skills:
        return "Please enter at least one valid skill.", 400

    # Save student profile in database
    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO student_profiles
        (name, education, skills, interest, domain, experience)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            education,
            ", ".join(skills),
            interest,
            domain,
            experience
        )
    )

    student_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # Create student profile text
    student_profile = (
        "Skills: " + " ".join(skills) +
        " Interest: " + interest +
        " Career domain: " + domain +
        " Education: " + education +
        " Experience: " + experience
    )

    # Create career profile text
    career_profiles = []

    for career in careers:

        profile = (
            career["name"] + " " +
            career["interest"] + " " +
            career["domain"] + " " +
            " ".join(career["skills"]) + " " +
            career["description"]
        )

        career_profiles.append(profile)

    # Convert text into numerical vectors
    vectorizer = TfidfVectorizer()

    all_profiles = [student_profile] + career_profiles

    tfidf_matrix = vectorizer.fit_transform(all_profiles)

    # Calculate similarity scores
    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    results = []

    for i, career in enumerate(careers):

        matched_skills = [
            skill for skill in skills
            if skill in career["skills"]
        ]

        missing_skills = [
            skill for skill in career["skills"]
            if skill not in matched_skills
        ]

        score = round(similarity[i] * 100)

        results.append({
            "name": career["name"],
            "score": score,
            "matched": matched_skills,
            "missing": missing_skills,
            "description": career["description"]
        })

    # Rank careers by similarity
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Select top 3 careers
    top_careers = results[:3]

    # Save recommendation results in database
    conn = get_db_connection()

    for career in top_careers:

        conn.execute(
            """
            INSERT INTO recommendation_results
            (student_id, career_name, score, matched_skills, missing_skills)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_id,
                career["name"],
                career["score"],
                ", ".join(career["matched"]),
                ", ".join(career["missing"])
            )
        )

    conn.commit()
    conn.close()

    # Display recommendation dashboard
    return render_template(
        "result.html",
        name=name,
        education=education,
        experience=experience,
        recommendations=top_careers
    )


if __name__ == "__main__":
    app.run(debug=True)
