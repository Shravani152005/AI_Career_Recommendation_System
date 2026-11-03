# CareerAI – AI-Based Career Recommendation System

## Project Overview
CareerAI is a web-based career recommendation application designed to help students identify suitable career paths based on their education, skills, interests, preferred domain, and experience.

The application uses Natural Language Processing (NLP) techniques and machine learning similarity measures to compare student profiles with predefined career profiles and recommend the most relevant career options.

## Features
- Student profile assessment
- Skill and interest-based career recommendations
- Top 3 career suggestions
- Matched and missing skill identification
- Career details and descriptions
- Recommendation history
- SQLite database for storing student profiles and results
- Input validation

## Technologies Used
- **Frontend:** HTML, CSS
- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn
- **NLP Technique:** TF-IDF Vectorization
- **Similarity Measure:** Cosine Similarity
- **Database:** SQLite

## How It Works
1. Students enter their personal and educational details.
2. They provide their skills, interests, and preferred career domain.
3. The system converts the profile information into numerical text representations using TF-IDF.
4. Cosine similarity compares the student profile with available career profiles.
5. The system displays the three most relevant career recommendations.
6. Students can explore career details and view previous recommendations.

## Available Career Paths
- Software Developer
- AI / Machine Learning Engineer
- Data Scientist
- Web Developer
- Cybersecurity Analyst
- DevOps Engineer
- Cloud Engineer
- UI/UX Designer
- Mobile App Developer
- Database Administrator

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Shravani152005/AI_Career_Recommendation_System.git
```

### 2. Open the Project Folder
```bash
cd AI_Career_Recommandation_System
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
```

### 4. Activate the Virtual Environment
```bash
venv\Scripts\activate
```

### 5. Install Required Packages
```bash
pip install flask scikit-learn
```

### 6. Run the Application
```bash
python app.py
```

### 7. Open in Browser
Visit:
```text
http://127.0.0.1:5000
```

## Project Structure
```text
AI_Career_Recommandation_System/
│
├── app.py
├── careerai.db
├── templates/
│   ├── index.html
│   ├── assessment.html
│   ├── result.html
│   ├── career.html
│   └── history.html
│
├── static/
│   └── style.css
│
└── README.md
```

## Future Enhancements
- Integration with real-time job opportunities
- User authentication and personalized dashboards
- Training with larger student-career datasets
- Improved recommendation techniques
- Resume analysis and skill-gap suggestions

## Note
Career recommendations are generated using TF-IDF and cosine similarity against predefined career profiles. The similarity scores indicate textual relevance and should not be interpreted as job-selection probabilities or model accuracy.

## Author
Developed as an academic project to support students in exploring suitable career opportunities.
