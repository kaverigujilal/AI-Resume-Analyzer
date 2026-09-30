import os
import json

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GET GEMINI API KEY
# =========================================================

API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# STREAMLIT CLOUD SECRET FALLBACK
# =========================================================

if not API_KEY:

    try:
        import streamlit as st

        API_KEY = st.secrets.get("GEMINI_API_KEY")

    except Exception:
        API_KEY = None


# =========================================================
# CHECK API KEY
# =========================================================

if not API_KEY:

    raise RuntimeError(
        "GEMINI_API_KEY not found. "
        "Add it to your local .env file or "
        "Streamlit Cloud Secrets."
    )


# =========================================================
# CONFIGURE GEMINI
# =========================================================

client = genai.Client(
    api_key=API_KEY
)


# =========================================================
# ANALYZE RESUME
# =========================================================

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are a professional ATS resume analyzer.

Analyze the resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add any explanation outside the JSON.

Use exactly this structure:

{{
    "ats_score": 0,
    "job_match_score": 0,
    "keyword_score": 0,
    "skills_score": 0,
    "resume_quality_score": 0,
    "experience_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "keywords": [],
    "suitable_roles": [],
    "strengths": [],
    "weaknesses": [],
    "improvements": [],
    "final_feedback": ""
}}

Rules:

- ats_score must be a number from 0 to 100.
- job_match_score must be a number from 0 to 100.
- keyword_score must be a number from 0 to 100.
- skills_score must be a number from 0 to 100.
- resume_quality_score must be a number from 0 to 100.
- experience_score must be a number from 0 to 100.

- The ATS score should represent the overall compatibility
  between the resume and the job description.

- Do not invent skills or experience.

- matching_skills must contain skills that are actually
  present in the resume and relevant to the job description.

- missing_skills should contain important skills or
  qualifications mentioned in the job description that
  are missing from the resume.

- keywords should contain important keywords from the
  job description.

- suitable_roles should contain realistic entry-level
  roles based on the resume.

- strengths must be based only on the resume.

- weaknesses must be based only on the resume.

- improvements should be practical and relevant to the
  target job.

- final_feedback should be professional and concise.

- Return valid JSON only.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        result = json.loads(text)

        required_fields = [
            "ats_score",
            "job_match_score",
            "keyword_score",
            "skills_score",
            "resume_quality_score",
            "experience_score",
            "matching_skills",
            "missing_skills",
            "keywords",
            "suitable_roles",
            "strengths",
            "weaknesses",
            "improvements",
            "final_feedback"
        ]

        for field in required_fields:

            if field not in result:

                raise ValueError(
                    f"Gemini response is missing field: {field}"
                )

        score_fields = [
            "ats_score",
            "job_match_score",
            "keyword_score",
            "skills_score",
            "resume_quality_score",
            "experience_score"
        ]

        for field in score_fields:

            try:

                result[field] = float(
                    result[field]
                )

            except (ValueError, TypeError):

                result[field] = 0

            result[field] = max(
                0,
                min(
                    100,
                    result[field]
                )
            )

        result["ats_score"] = round(result["ats_score"])
        result["job_match_score"] = round(result["job_match_score"])
        result["keyword_score"] = round(result["keyword_score"])
        result["skills_score"] = round(result["skills_score"])
        result["resume_quality_score"] = round(result["resume_quality_score"])
        result["experience_score"] = round(result["experience_score"])

        return result

    except Exception as e:

        error_text = str(e)

        if (
            "429" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
        ):

            raise RuntimeError(
                "Gemini API quota has been exceeded. "
                "Please wait for the quota to reset and try again."
            )

        if (
            "401" in error_text
            or "403" in error_text
            or "API_KEY_INVALID" in error_text
            or "API key not valid" in error_text
        ):

            raise RuntimeError(
                "Gemini API authentication failed. "
                "Please check the Gemini API key in "
                "your .env file or Streamlit Secrets."
            )

        raise RuntimeError(
            f"Gemini API error: {error_text}"
        )