import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


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

Analyze the candidate's resume against the target job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Your task is to evaluate how well the resume matches the
specific job description.

IMPORTANT RULES:

1. Do not invent skills, education, experience, projects,
   certifications, or achievements.

2. Only consider a skill as a matching skill if it is
   actually present in the resume.

3. Missing skills should contain important requirements
   from the job description that are not clearly present
   in the resume.

4. Keywords should contain important technical and
   professional keywords from the job description.

5. Suitable roles must be realistic entry-level roles
   based on the actual resume.

6. Strengths must be based only on information present
   in the resume.

7. Weaknesses must be based only on information present
   in the resume and its comparison with the job.

8. Improvements should be practical and relevant to
   the target job.

9. Be realistic when evaluating a student or fresher.
   Do not penalize a student as heavily as an experienced
   professional simply because they lack years of experience.

10. All scores must be integers between 0 and 100.

SCORING GUIDELINES:

ATS score:
Overall compatibility between the resume and job description.

Job match score:
How closely the candidate's background matches the job.

Keyword score:
How many important job-description keywords are represented
in the resume.

Skills score:
How closely the candidate's technical skills match the
required technical skills.

Resume quality score:
Quality, clarity, structure, education, projects,
skills, contact information, links, and overall
resume completeness.

Experience score:
Relevant projects, internships, practical work,
certifications, GitHub/portfolio evidence, and
other practical experience. Consider the candidate's
student/fresher status.

Return the result using exactly these fields:

- ats_score
- job_match_score
- keyword_score
- skills_score
- resume_quality_score
- experience_score
- matching_skills
- missing_skills
- keywords
- suitable_roles
- strengths
- weaknesses
- improvements
- final_feedback

All list fields must contain strings.

final_feedback must be a concise professional paragraph.

Do not invent information that is not present in the resume.
"""


    try:

        # =================================================
        # GEMINI REQUEST
        # =================================================

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )


        # =================================================
        # GET RESPONSE TEXT
        # =================================================

        text = response.text.strip()


        # =================================================
        # PARSE JSON
        # =================================================

        result = json.loads(text)


        # =================================================
        # REQUIRED FIELDS
        # =================================================

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


        # =================================================
        # SCORE FIELDS
        # =================================================

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


            # Keep score between 0 and 100

            result[field] = max(
                0,
                min(
                    100,
                    result[field]
                )
            )


        # =================================================
        # ROUND SCORES
        # =================================================

        result["ats_score"] = round(
            result["ats_score"]
        )

        result["job_match_score"] = round(
            result["job_match_score"]
        )

        result["keyword_score"] = round(
            result["keyword_score"]
        )

        result["skills_score"] = round(
            result["skills_score"]
        )

        result["resume_quality_score"] = round(
            result["resume_quality_score"]
        )

        result["experience_score"] = round(
            result["experience_score"]
        )


        # =================================================
        # ENSURE LIST FIELDS ARE LISTS
        # =================================================

        list_fields = [
            "matching_skills",
            "missing_skills",
            "keywords",
            "suitable_roles",
            "strengths",
            "weaknesses",
            "improvements"
        ]


        for field in list_fields:

            if not isinstance(
                result[field],
                list
            ):

                result[field] = [
                    str(result[field])
                ]


            result[field] = [
                str(item)
                for item in result[field]
            ]


        # =================================================
        # ENSURE FINAL FEEDBACK IS TEXT
        # =================================================

        result["final_feedback"] = str(
            result["final_feedback"]
        )


        # =================================================
        # RETURN FINAL RESULT
        # =================================================

        return result


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        error_text = str(e)


        # =================================================
        # QUOTA / RATE LIMIT ERROR
        # =================================================

        if (
            "429" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
        ):

            raise RuntimeError(
                "Gemini API quota has been exceeded. "
                "Please wait for the quota to reset and try again."
            )


        # =================================================
        # AUTHENTICATION ERROR
        # =================================================

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


        # =================================================
        # MODEL NOT FOUND / UNAVAILABLE
        # =================================================

        if (
            "404" in error_text
            or "NOT_FOUND" in error_text
            or "no longer available" in error_text.lower()
        ):

            raise RuntimeError(
                "The selected Gemini model is unavailable. "
                "Please use a currently supported Gemini model."
            )


        # =================================================
        # TEMPORARY SERVER ERROR
        # =================================================

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
            or "high demand" in error_text.lower()
        ):

            raise RuntimeError(
                "Gemini is temporarily experiencing high demand. "
                "Please try again in a few moments."
            )


        # =================================================
        # OTHER GEMINI ERROR
        # =================================================

        raise RuntimeError(
            f"Gemini API error: {error_text}"
        )