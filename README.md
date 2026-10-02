# AI Resume Analyzer 🤖📄

An AI-powered resume analysis application that compares a candidate's resume with a target job description and provides ATS-style compatibility analysis, skill matching, keyword analysis, suitable roles, and practical improvement suggestions.

## 🚀 Live Demo

**Streamlit App:**  
https://ai-resume-analyzer-9esb9hv39tbpid5du5ac9c.streamlit.app/

**GitHub Repository:**  
https://github.com/kaverigujilal/AI-Resume-Analyzer

---

## ✨ Features

- 📄 Upload PDF resumes
- 🤖 AI-powered resume analysis using Google Gemini
- 🎯 ATS compatibility score
- 📊 Job match score
- 🔑 Keyword match analysis
- 🧠 Technical skills matching
- ❌ Missing skills detection
- 💼 Suitable entry-level role suggestions
- 💪 Resume strengths analysis
- ⚠️ Resume weaknesses analysis
- 🚀 Practical resume improvement suggestions
- 📑 Downloadable PDF analysis report
- 💻 Demo / Local Mode without Gemini API usage
- 🔐 Secure API-key handling using environment variables and Streamlit Secrets
- ☁️ Streamlit Cloud deployment

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- PyMuPDF
- ReportLab
- python-dotenv
- JSON
- Git
- GitHub

---

## 🧠 How It Works

```text
Resume PDF
    ↓
PDF Text Extraction
    ↓
Resume + Job Description
    ↓
Gemini AI Analysis
    ↓
Structured JSON Response
    ↓
ATS & Skill Analysis
    ↓
Results Dashboard
    ↓
Downloadable PDF Report
## 🔐 Gemini API Setup
Create a `.env` file in the project folder.
Add your Gemini API key to the `.env` file.
GEMINI_API_KEY=your_api_key_here
Never upload your API key to GitHub.
The `.env` file is protected using `.gitignore`.