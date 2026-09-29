import re


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {

    "python": ["python", "python programming"],
    "java": ["java", "java programming"],
    "c++": ["c++", "cpp"],
    "c": ["c programming"],
    "javascript": ["javascript", "java script", "js"],
    "typescript": ["typescript", "ts"],

    "html": ["html", "html5"],
    "css": ["css", "css3"],

    "sql": ["sql", "structured query language"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],

    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],
    "generative ai": [
        "generative ai",
        "genai",
        "generative artificial intelligence"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "computer vision": [
        "computer vision",
        "cv"
    ],

    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "scikit-learn": [
        "scikit-learn",
        "sklearn",
        "scikit learn"
    ],

    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],

    "langchain": ["langchain"],

    "rag": [
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation"
    ],

    "llm": [
        "llm",
        "large language model",
        "large language models"
    ],

    "openai": ["openai", "open ai"],
    "gemini": ["gemini", "google gemini"],
    "hugging face": ["hugging face", "huggingface"],

    "git": ["git"],
    "github": ["github", "git hub"],

    "docker": ["docker"],
    "streamlit": ["streamlit"],

    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "django": ["django"],

    "react": [
        "react",
        "react.js",
        "reactjs"
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "rest api": [
        "rest api",
        "restful api",
        "restful apis",
        "api development"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform"
    ],

    "data structures": [
        "data structures",
        "data structure",
        "dsa"
    ],

    "algorithms": [
        "algorithms",
        "algorithm"
    ],

    "problem solving": [
        "problem solving",
        "problem-solving"
    ],

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "excel": [
        "excel",
        "microsoft excel"
    ],

    "tableau": ["tableau"],

    "data analysis": [
        "data analysis",
        "data analytics",
        "data analyst"
    ],

    "data visualization": [
        "data visualization",
        "data visualisation"
    ],

    "statistics": [
        "statistics",
        "statistical analysis"
    ],

    "api": [
        "api",
        "apis",
        "application programming interface"
    ],

    "oop": [
        "oop",
        "object oriented programming",
        "object-oriented programming"
    ]
}


# =========================================================
# SOFT SKILLS
# =========================================================

SOFT_SKILLS = [

    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "problem-solving",
    "time management",
    "analytical thinking",
    "critical thinking",
    "adaptability",
    "collaboration",
    "creativity",
    "attention to detail",
    "presentation skills",
    "interpersonal skills",
    "organizational skills"
]


# =========================================================
# EDUCATION TERMS
# =========================================================

EDUCATION_KEYWORDS = [

    "b.tech",
    "btech",
    "b.e",
    "be degree",
    "bachelor",
    "bachelors",
    "bachelor's",
    "computer science",
    "information technology",
    "artificial intelligence",
    "machine learning",
    "engineering degree",
    "engineering",
    "degree",
    "graduation",
    "undergraduate",
    "postgraduate",
    "master",
    "m.tech",
    "mtech"
]


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    text = str(text).lower()

    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# CHECK SKILL
# =========================================================

def contains_skill(
    text,
    aliases
):

    normalized_text = normalize_text(
        text
    )

    for alias in aliases:

        alias = normalize_text(
            alias
        )

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(alias)
            + r"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            normalized_text
        ):

            return True

    return False


# =========================================================
# FIND TECHNICAL SKILLS
# =========================================================

def find_skills(text):

    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        if contains_skill(
            text,
            aliases
        ):

            found_skills.append(
                skill
            )

    return found_skills


# =========================================================
# FIND SOFT SKILLS
# =========================================================

def find_soft_skills(text):

    normalized_text = normalize_text(
        text
    )

    found = []

    for skill in SOFT_SKILLS:

        if skill in normalized_text:

            if skill not in found:

                found.append(
                    skill
                )

    return found


# =========================================================
# FIND EDUCATION TERMS
# =========================================================

def find_education_requirements(text):

    normalized_text = normalize_text(
        text
    )

    found = []

    for keyword in EDUCATION_KEYWORDS:

        if keyword in normalized_text:

            if keyword not in found:

                found.append(
                    keyword
                )

    return found


# =========================================================
# EXTRACT IMPORTANT KEYWORDS
# =========================================================

def extract_keywords(
    job_description
):

    job_lower = normalize_text(
        job_description
    )

    keywords = []

    # Technical skills get highest priority.
    technical_skills = find_skills(
        job_lower
    )

    for skill in technical_skills:

        if skill not in keywords:

            keywords.append(
                skill
            )


    # Soft skills.
    soft_skills = find_soft_skills(
        job_lower
    )

    for skill in soft_skills:

        if skill not in keywords:

            keywords.append(
                skill
            )


    # Education.
    education_terms = (
        find_education_requirements(
            job_lower
        )
    )

    for term in education_terms:

        if term not in keywords:

            keywords.append(
                term
            )


    # Role-specific terms.
    role_terms = [

        "ai engineer",
        "ml engineer",
        "machine learning engineer",
        "data analyst",
        "data scientist",
        "python developer",
        "software developer",
        "backend developer",
        "frontend developer",
        "full stack developer",
        "generative ai engineer",
        "genai engineer",
        "developer",
        "engineer",
        "analyst",
        "intern",
        "internship"
    ]

    for term in role_terms:

        if term in job_lower:

            if term not in keywords:

                keywords.append(
                    term
                )

    return list(
        dict.fromkeys(
            keywords
        )
    )[:50]


# =========================================================
# KEYWORD MATCH
# =========================================================

def calculate_keyword_match(
    keywords,
    resume_text
):

    resume_lower = normalize_text(
        resume_text
    )

    matching = []
    missing = []

    for keyword in keywords:

        keyword = normalize_text(
            keyword
        )

        if keyword in resume_lower:

            matching.append(
                keyword
            )

        else:

            missing.append(
                keyword
            )

    return matching, missing


# =========================================================
# RESUME QUALITY
# =========================================================

def calculate_resume_quality(
    resume_text
):

    resume_lower = normalize_text(
        resume_text
    )

    score = 0

    checks = {

        "education": (
            "education" in resume_lower
            or "academic" in resume_lower
        ),

        "skills": (
            "skills" in resume_lower
            or "technical skills" in resume_lower
        ),

        "projects": (
            "project" in resume_lower
            or "projects" in resume_lower
        ),

        "experience": (
            "experience" in resume_lower
            or "internship" in resume_lower
        ),

        "certification": (
            "certification" in resume_lower
            or "certificate" in resume_lower
        ),

        "contact": (
            "@" in resume_lower
            or "contact" in resume_lower
            or "phone" in resume_lower
        ),

        "linkedin": (
            "linkedin" in resume_lower
        ),

        "github": (
            "github" in resume_lower
        )
    }


    points = {

        "education": 15,
        "skills": 15,
        "projects": 15,
        "experience": 15,
        "certification": 10,
        "contact": 10,
        "linkedin": 5,
        "github": 5
    }


    for section, exists in checks.items():

        if exists:

            score += points[
                section
            ]


    # Resume length should not strongly
    # penalize students.
    if len(resume_lower) >= 400:

        score += 5

    if len(resume_lower) >= 800:

        score += 5


    return min(
        score,
        100
    )


# =========================================================
# EXPERIENCE SCORE
# =========================================================

def calculate_experience_score(
    resume_text
):

    resume_lower = normalize_text(
        resume_text
    )

    score = 0


    # Professional experience.
    if "experience" in resume_lower:

        score += 25


    # Internship experience.
    if "internship" in resume_lower:

        score += 25


    # Projects are especially important
    # for students.
    if (
        "project" in resume_lower
        or "projects" in resume_lower
    ):

        score += 25


    # GitHub demonstrates practical work.
    if "github" in resume_lower:

        score += 10


    # Certifications demonstrate learning.
    if (
        "certification" in resume_lower
        or "certificate" in resume_lower
    ):

        score += 10


    # Practical / hands-on work.
    if (
        "developed" in resume_lower
        or "built" in resume_lower
        or "implemented" in resume_lower
    ):

        score += 5


    return min(
        score,
        100
    )


# =========================================================
# SUITABLE ROLES
# =========================================================

def find_suitable_roles(
    resume_text
):

    roles = []


    if (
        contains_skill(
            resume_text,
            SKILL_ALIASES["python"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["machine learning"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["artificial intelligence"]
        )
    ):

        roles.append(
            "AI/ML Intern"
        )


    if (
        contains_skill(
            resume_text,
            SKILL_ALIASES["generative ai"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["llm"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["langchain"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["rag"]
        )
    ):

        roles.append(
            "Generative AI Intern"
        )


    if contains_skill(
        resume_text,
        SKILL_ALIASES["python"]
    ):

        roles.append(
            "Python Developer Intern"
        )


    if (
        contains_skill(
            resume_text,
            SKILL_ALIASES["sql"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["mysql"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["pandas"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["excel"]
        )
    ):

        roles.append(
            "Data Analyst Intern"
        )


    if contains_skill(
        resume_text,
        SKILL_ALIASES["machine learning"]
    ):

        roles.append(
            "Machine Learning Intern"
        )


    if contains_skill(
        resume_text,
        SKILL_ALIASES["react"]
    ):

        roles.append(
            "Frontend Developer Intern"
        )


    if (
        contains_skill(
            resume_text,
            SKILL_ALIASES["node.js"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["fastapi"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["flask"]
        )
        or contains_skill(
            resume_text,
            SKILL_ALIASES["django"]
        )
    ):

        roles.append(
            "Backend Developer Intern"
        )


    if not roles:

        roles.append(
            "Software Developer Intern"
        )


    return list(
        dict.fromkeys(
            roles
        )
    )


# =========================================================
# JOB DESCRIPTION ANALYSIS
# =========================================================

def analyze_job_description(
    job_description
):

    job_lower = normalize_text(
        job_description
    )

    detected_skills = find_skills(
        job_lower
    )

    keywords = extract_keywords(
        job_description
    )

    experience_requirements = []

    experience_patterns = [

        r"\d+\+?\s*years?\s*(?:of\s*)?experience",

        r"\d+\s*-\s*\d+\s*years?\s*(?:of\s*)?experience",

        r"freshers?",

        r"entry[- ]level",

        r"internship experience",

        r"intern"
    ]


    for pattern in experience_patterns:

        matches = re.findall(
            pattern,
            job_lower
        )

        for match in matches:

            if match not in experience_requirements:

                experience_requirements.append(
                    match
                )


    education_requirements = (
        find_education_requirements(
            job_lower
        )
    )

    soft_skills = find_soft_skills(
        job_lower
    )


    # =====================================================
    # ROLE TYPE
    # =====================================================

    role_type = "General Technology Role"


    if (
        "generative ai" in job_lower
        or "genai" in job_lower
        or "llm" in job_lower
        or "rag" in job_lower
    ):

        role_type = (
            "Generative AI / LLM Role"
        )


    elif (
        "machine learning" in job_lower
        or "ml intern" in job_lower
        or "ml engineer" in job_lower
    ):

        role_type = (
            "AI / Machine Learning Role"
        )


    elif (
        "data analyst" in job_lower
        or "data analysis" in job_lower
        or "power bi" in job_lower
        or "tableau" in job_lower
    ):

        role_type = (
            "Data Analytics Role"
        )


    elif (
        "full stack" in job_lower
        or "full-stack" in job_lower
    ):

        role_type = (
            "Full Stack Development Role"
        )


    elif (
        "frontend" in job_lower
        or "front-end" in job_lower
        or "react" in job_lower
        or "javascript" in job_lower
    ):

        role_type = (
            "Frontend Development Role"
        )


    elif (
        "backend" in job_lower
        or "back-end" in job_lower
        or "fastapi" in job_lower
        or "flask" in job_lower
        or "django" in job_lower
    ):

        role_type = (
            "Backend Development Role"
        )


    elif (
        "python developer" in job_lower
        or "python development" in job_lower
    ):

        role_type = (
            "Python Development Role"
        )


    return {

        "detected_skills":
            detected_skills,

        "keywords":
            keywords,

        "experience_requirements":
            experience_requirements,

        "education_requirements":
            education_requirements,

        "soft_skills":
            soft_skills,

        "role_type":
            role_type,

        "total_requirements":
            (
                len(detected_skills)
                + len(soft_skills)
                + len(education_requirements)
            )
    }


# =========================================================
# MAIN ANALYZER
# =========================================================

def get_demo_result(
    resume_text,
    job_description
):

    resume_lower = normalize_text(
        resume_text
    )

    job_lower = normalize_text(
        job_description
    )


    # =====================================================
    # FIND RESUME SKILLS
    # =====================================================

    resume_skills = find_skills(
        resume_lower
    )


    # =====================================================
    # FIND JOB SKILLS
    # =====================================================

    job_skills = find_skills(
        job_lower
    )


    # =====================================================
    # MATCHING SKILLS
    # =====================================================

    matching_skills = []

    for skill in job_skills:

        if skill in resume_skills:

            matching_skills.append(
                skill
            )


    # =====================================================
    # MISSING SKILLS
    # =====================================================

    missing_skills = []

    for skill in job_skills:

        if skill not in resume_skills:

            missing_skills.append(
                skill
            )


    # =====================================================
    # KEYWORDS
    # =====================================================

    keywords = extract_keywords(
        job_description
    )


    matching_keywords, missing_keywords = (
        calculate_keyword_match(
            keywords,
            resume_lower
        )
    )


    # =====================================================
    # KEYWORD SCORE
    # =====================================================

    if keywords:

        keyword_score = round(
            (
                len(matching_keywords)
                / len(keywords)
            ) * 100
        )

    else:

        keyword_score = 0


    keyword_score = max(
        0,
        min(
            100,
            keyword_score
        )
    )


    # =====================================================
    # SKILLS SCORE
    # =====================================================

    if job_skills:

        skills_score = round(
            (
                len(matching_skills)
                / len(job_skills)
            ) * 100
        )

    else:

        skills_score = 50


    skills_score = max(
        0,
        min(
            100,
            skills_score
        )
    )


    # =====================================================
    # SOFT SKILL SCORE
    # =====================================================

    job_soft_skills = find_soft_skills(
        job_lower
    )

    resume_soft_skills = find_soft_skills(
        resume_lower
    )


    matching_soft_skills = [

        skill

        for skill in job_soft_skills

        if skill in resume_soft_skills
    ]


    if job_soft_skills:

        soft_skill_score = round(
            (
                len(matching_soft_skills)
                / len(job_soft_skills)
            ) * 100
        )

    else:

        soft_skill_score = 50


    # =====================================================
    # JOB MATCH SCORE
    # =====================================================

    if job_skills:

        technical_match = (
            skills_score
        )

    else:

        technical_match = 50


    job_match_score = round(

        technical_match * 0.60

        + keyword_score * 0.25

        + soft_skill_score * 0.15

    )


    job_match_score = max(
        0,
        min(
            100,
            job_match_score
        )
    )


    # =====================================================
    # RESUME QUALITY
    # =====================================================

    resume_quality_score = (
        calculate_resume_quality(
            resume_lower
        )
    )


    # =====================================================
    # EXPERIENCE
    # =====================================================

    experience_score = (
        calculate_experience_score(
            resume_lower
        )
    )


    # =====================================================
    # ATS SCORE
    # =====================================================

    ats_score = round(

        job_match_score * 0.40

        + skills_score * 0.25

        + keyword_score * 0.15

        + resume_quality_score * 0.15

        + experience_score * 0.05

    )


    ats_score = max(
        0,
        min(
            100,
            ats_score
        )
    )


    # =====================================================
    # JOB ANALYSIS
    # =====================================================

    job_analysis = (
        analyze_job_description(
            job_description
        )
    )


    # =====================================================
    # SUITABLE ROLES
    # =====================================================

    suitable_roles = (
        find_suitable_roles(
            resume_lower
        )
    )


    # =====================================================
    # STRENGTHS
    # =====================================================

    strengths = []


    if resume_skills:

        strengths.append(
            f"{len(resume_skills)} technical skills "
            "were detected in the resume"
        )


    if matching_skills:

        strengths.append(
            f"{len(matching_skills)} job-required "
            "technical skills match"
        )


    if (
        "project" in resume_lower
        or "projects" in resume_lower
    ):

        strengths.append(
            "Projects demonstrate practical experience"
        )


    if "internship" in resume_lower:

        strengths.append(
            "Internship experience is mentioned"
        )


    if "github" in resume_lower:

        strengths.append(
            "GitHub profile or project work is mentioned"
        )


    if "linkedin" in resume_lower:

        strengths.append(
            "LinkedIn profile is mentioned"
        )


    if not strengths:

        strengths.append(
            "Resume content was successfully extracted"
        )


    # =====================================================
    # WEAKNESSES
    # =====================================================

    weaknesses = []


    if missing_skills:

        weaknesses.append(
            f"{len(missing_skills)} job-required "
            "technical skills were not detected"
        )


    if keyword_score < 50:

        weaknesses.append(
            "Job-specific keyword coverage could be improved"
        )


    if "github" not in resume_lower:

        weaknesses.append(
            "GitHub is not clearly mentioned"
        )


    if (
        "project" not in resume_lower
        and "projects" not in resume_lower
    ):

        weaknesses.append(
            "Projects are not clearly mentioned"
        )


    if not weaknesses:

        weaknesses.append(
            "No major structural weaknesses detected"
        )


    # =====================================================
    # IMPROVEMENTS
    # =====================================================

    improvements = []


    if missing_skills:

        improvements.append(
            "Add missing job-related skills only if "
            "you genuinely possess them"
        )


    if keyword_score < 60:

        improvements.append(
            "Use relevant terminology from the job "
            "description where it truthfully describes "
            "your projects or experience"
        )


    if "github" not in resume_lower:

        improvements.append(
            "Add GitHub and upload relevant projects"
        )


    if (
        "project" not in resume_lower
        and "projects" not in resume_lower
    ):

        improvements.append(
            "Add 2-3 relevant academic or personal projects"
        )


    if experience_score < 50:

        improvements.append(
            "Add practical projects, internships, "
            "certifications, or hands-on work"
        )


    improvements.append(
        "Use measurable results when describing "
        "projects and achievements"
    )


    # =====================================================
    # FINAL FEEDBACK
    # =====================================================

    final_feedback = (

        f"The resume has an estimated ATS compatibility "
        f"score of {ats_score}/100 for this job description. "

        f"It matches {len(matching_skills)} of "
        f"{len(job_skills)} detected technical skills "
        f"and {len(matching_keywords)} of "
        f"{len(keywords)} relevant keywords. "

        "For an entry-level candidate, practical projects, "
        "relevant skills, GitHub work, and truthful "
        "job-specific terminology can improve the match."
    )


    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "ats_score":
            ats_score,

        "job_match_score":
            job_match_score,

        "keyword_score":
            keyword_score,

        "skills_score":
            skills_score,

        "resume_quality_score":
            resume_quality_score,

        "experience_score":
            experience_score,

        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills,

        "keywords":
            keywords,

        "suitable_roles":
            suitable_roles,

        "strengths":
            strengths,

        "weaknesses":
            weaknesses,

        "improvements":
            improvements,

        "final_feedback":
            final_feedback,

        "job_analysis":
            job_analysis
    }