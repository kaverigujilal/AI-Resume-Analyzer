import os
import json

from dotenv import load_dotenv
import google.generativeai as genai


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found in .env file."
    )


# =========================================================
# CONFIGURE GEMINI
# =========================================================

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-3.8-flash"
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

        response = model.generate_content(prompt)

        text = response.text.strip()

        # =================================================
        # REMOVE MARKDOWN CODE BLOCKS IF GEMINI ADDS THEM
        # =================================================

        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # =================================================
        # CONVERT JSON TEXT TO PYTHON DICTIONARY
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

        # =================================================
        # CHECK REQUIRED FIELDS
        # =================================================

        for field in required_fields:

            if field not in result:

                raise ValueError(
                    f"Gemini response is missing field: {field}"
                )

        # =================================================
        # MAKE SURE SCORES ARE NUMBERS
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

            # Keep scores between 0 and 100

            result[field] = max(
                0,
                min(
                    100,
                    result[field]
                )
            )

        # =================================================
        # CONVERT ATS SCORE TO INTEGER IF POSSIBLE
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
        # RETURN RESULT
        # =================================================

        return result

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        error_text = str(e)

        # Gemini quota / rate limit

        if (
            "429" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
        ):

            raise RuntimeError(
                "Gemini API quota has been exceeded. "
                "Please wait for the quota to reset and try again."
            )

        # Other Gemini errors

        raise RuntimeError(
            f"Gemini API error: {error_text}"
        )