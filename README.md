# AI Resume Analyzer

An AI-powered resume analysis application that compares a candidate's resume with a job description and provides ATS-style scoring, skill matching, keyword analysis, suitable roles, and improvement suggestions.

## 🚀 Features

- 📄 Upload a resume in PDF format
- 🎯 Generate an ATS compatibility score
- 📊 Analyze job match score
- 🔑 Identify important job-description keywords
- 🛠️ Compare resume skills with required skills
- ❌ Identify missing skills
- 💼 Suggest suitable entry-level job roles
- 💪 Identify resume strengths
- ⚠️ Identify resume weaknesses
- 💡 Provide practical resume improvement suggestions
- 📑 Generate a downloadable PDF report
- 🤖 Gemini AI analysis mode
- 💻 Demo / Local analysis mode for testing without API usage
- 🔐 Protect API credentials using `.env`

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- PyMuPDF
- ReportLab
- python-dotenv
- JSON

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── ai_analyzer.py
├── demo_data.py
├── pdf_report.py
├── resume_parser.py
├── app_backup.py
├── README.md
├── .gitignore
└── .env