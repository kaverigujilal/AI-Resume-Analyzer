import streamlit as st

from resume_parser import extract_text_from_pdf
from demo_data import get_demo_result
from pdf_report import create_pdf_report


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    /* Section headings */
    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #111827;
        margin-top: 28px;
        margin-bottom: 15px;
    }

    /* Score card */
    .score-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
    }

    .score-number {
        font-size: 34px;
        font-weight: 800;
        color: #2563eb;
    }

    .score-label {
        font-size: 15px;
        color: #6b7280;
        margin-top: 5px;
    }

    /* Information cards */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-bottom: 12px;
    }

    /* Small badge */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        background: #eef2ff;
        color: #4338ca;
        font-size: 13px;
        font-weight: 600;
        margin: 3px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        margin-top: 35px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume against a job description and improve your ATS compatibility.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ Settings")

    demo_mode = st.toggle(
        "Demo / Local Mode",
        value=True
    )

    if demo_mode:

        st.success("Local analysis enabled.")

        st.caption(
            "Uses your local resume-analysis engine. "
            "No Gemini API request is required."
        )

    else:

        st.warning("AI Mode enabled.")

        st.caption(
            "AI Mode uses the Gemini API. "
            "If your Gemini quota is unavailable, "
            "switch back to Demo / Local Mode."
        )

    st.markdown("---")

    st.subheader("📌 How it works")

    st.write("1️⃣ Upload your resume")
    st.write("2️⃣ Paste the job description")
    st.write("3️⃣ Analyze your resume")
    st.write("4️⃣ Review ATS compatibility")
    st.write("5️⃣ Improve your resume")
    st.write("6️⃣ Download the report")

    st.markdown("---")

    st.caption(
        "AI Resume Analyzer\n"
        "Python • Streamlit • PyMuPDF • Gemini"
    )


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    '<div class="section-title">1️⃣ Upload Your Resume</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"],
    help="Upload a text-based PDF resume."
)


if uploaded_file:

    st.success(
        f"✅ Resume uploaded: {uploaded_file.name}"
    )


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.markdown(
    '<div class="section-title">2️⃣ Paste Job Description</div>',
    unsafe_allow_html=True
)

job_description = st.text_area(
    "Job Description",
    height=260,
    placeholder=(
        "Paste the complete job description here...\n\n"
        "Example:\n"
        "We are looking for an AI/ML intern with Python, "
        "machine learning, SQL and data analysis skills."
    )
)


# =========================================================
# INPUT SUMMARY
# =========================================================

if uploaded_file or job_description.strip():

    st.markdown(
        '<div class="section-title">📋 Application Information</div>',
        unsafe_allow_html=True
    )

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        if uploaded_file:

            st.info(
                f"📄 Resume: **{uploaded_file.name}**"
            )

        else:

            st.info(
                "📄 Resume: Not uploaded"
            )

    with info_col2:

        if job_description.strip():

            word_count = len(job_description.split())

            st.info(
                f"📝 Job Description: **{word_count} words**"
            )

        else:

            st.info(
                "📝 Job Description: Not provided"
            )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.markdown("")

analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if uploaded_file is None:

        st.error(
            "⚠️ Please upload your resume PDF first."
        )

        st.stop()


    if not job_description.strip():

        st.error(
            "⚠️ Please paste a job description first."
        )

        st.stop()


    # -----------------------------------------------------
    # EXTRACT RESUME TEXT
    # -----------------------------------------------------

    with st.spinner("📖 Reading your resume..."):

        try:

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        except Exception as e:

            st.error(
                f"❌ Could not read the PDF: {e}"
            )

            st.stop()


    if not resume_text.strip():

        st.error(
            "❌ No readable text was found in the uploaded PDF."
        )

        st.stop()


    # -----------------------------------------------------
    # ANALYZE
    # -----------------------------------------------------

    with st.spinner("🤖 Analyzing your resume..."):

        try:

            if demo_mode:

                result = get_demo_result(
                    resume_text,
                    job_description
                )

            else:

                from ai_analyzer import analyze_resume

                result = analyze_resume(
                    resume_text,
                    job_description
                )

        except Exception as e:

            st.error(
                f"❌ {e}"
            )

            st.stop()


    # =====================================================
    # SUCCESS
    # =====================================================

    st.success(
        "✅ Resume analysis completed successfully!"
    )


    # =====================================================
    # ATS SCORE
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 ATS Compatibility</div>',
        unsafe_allow_html=True
    )

    ats_score = result["ats_score"]

    score_col1, score_col2, score_col3 = st.columns(
        [1, 2, 1]
    )

    with score_col2:

        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-number">
                    {ats_score}/100
                </div>
                <div class="score-label">
                    Overall ATS Score
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.progress(
        ats_score / 100
    )


    if ats_score >= 80:

        st.success(
            "🟢 Strong compatibility with this job description."
        )

    elif ats_score >= 60:

        st.info(
            "🟡 Moderate compatibility. "
            "Review the missing skills and keywords."
        )

    else:

        st.warning(
            "🔴 Lower compatibility. "
            "Review the missing skills, keywords and requirements."
        )


    # =====================================================
    # DETAILED SCORES
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Detailed Scores</div>',
        unsafe_allow_html=True
    )

    score_columns = st.columns(5)

    score_data = [
        (
            "🎯",
            "Job Match",
            result["job_match_score"]
        ),
        (
            "🔑",
            "Keyword Match",
            result["keyword_score"]
        ),
        (
            "🧠",
            "Skills Match",
            result["skills_score"]
        ),
        (
            "📄",
            "Resume Quality",
            result["resume_quality_score"]
        ),
        (
            "💼",
            "Experience",
            result["experience_score"]
        )
    ]

    for column, item in zip(
        score_columns,
        score_data
    ):

        icon, label, score = item

        with column:

            st.metric(
                f"{icon} {label}",
                f"{score}/100"
            )


    # =====================================================
    # RESUME LENGTH
    # =====================================================

    resume_word_count = len(
        resume_text.split()
    )

    st.metric(
        "📝 Resume Length",
        f"{resume_word_count} words"
    )


    # =====================================================
    # SCORE COMPARISON
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Score Breakdown</div>',
        unsafe_allow_html=True
    )

    score_items = [
        (
            "🎯 Job Match",
            result["job_match_score"]
        ),
        (
            "🔑 Keyword Match",
            result["keyword_score"]
        ),
        (
            "🧠 Skills Match",
            result["skills_score"]
        ),
        (
            "📄 Resume Quality",
            result["resume_quality_score"]
        ),
        (
            "💼 Experience",
            result["experience_score"]
        )
    ]

    for label, score in score_items:

        st.write(
            f"**{label} — {score}/100**"
        )

        st.progress(
            score / 100
        )


    # =====================================================
    # JOB DESCRIPTION ANALYSIS
    # =====================================================

    if "job_analysis" in result:

        job_analysis = result["job_analysis"]

        st.markdown(
            '<div class="section-title">'
            '🎯 Job Description Analysis'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            f"**Detected Role Type:** "
            f"{job_analysis['role_type']}"
        )


        jd_col1, jd_col2, jd_col3 = st.columns(3)

        with jd_col1:

            st.metric(
                "💻 Technical Skills",
                len(
                    job_analysis[
                        "detected_skills"
                    ]
                )
            )

        with jd_col2:

            st.metric(
                "🤝 Soft Skills",
                len(
                    job_analysis[
                        "soft_skills"
                    ]
                )
            )

        with jd_col3:

            st.metric(
                "🎓 Education Requirements",
                len(
                    job_analysis[
                        "education_requirements"
                    ]
                )
            )


        # -------------------------------------------------
        # TECHNICAL SKILLS
        # -------------------------------------------------

        st.subheader(
            "💻 Required Technical Skills"
        )

        technical_skills = job_analysis[
            "detected_skills"
        ]

        if technical_skills:

            for skill in technical_skills:

                st.markdown(
                    f'<span class="badge">{skill}</span>',
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "No specific technical skills detected."
            )


        # -------------------------------------------------
        # SOFT SKILLS
        # -------------------------------------------------

        st.subheader(
            "🤝 Soft Skills"
        )

        soft_skills = job_analysis[
            "soft_skills"
        ]

        if soft_skills:

            for skill in soft_skills:

                st.markdown(
                    f'<span class="badge">{skill}</span>',
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "No specific soft skills detected."
            )


        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        st.subheader(
            "💼 Experience Requirements"
        )

        experience_requirements = job_analysis[
            "experience_requirements"
        ]

        if experience_requirements:

            for item in experience_requirements:

                st.write(
                    f"• {item}"
                )

        else:

            st.write(
                "No specific experience requirement detected."
            )


        # -------------------------------------------------
        # EDUCATION
        # -------------------------------------------------

        st.subheader(
            "🎓 Education Requirements"
        )

        education_requirements = job_analysis[
            "education_requirements"
        ]

        if education_requirements:

            for item in education_requirements:

                st.write(
                    f"• {item}"
                )

        else:

            st.write(
                "No specific education requirement detected."
            )


    # =====================================================
    # SKILL ANALYSIS
    # =====================================================

    st.markdown(
        '<div class="section-title">🧠 Skill Analysis</div>',
        unsafe_allow_html=True
    )

    skill_col1, skill_col2 = st.columns(2)


    # -----------------------------------------------------
    # MATCHING SKILLS
    # -----------------------------------------------------

    with skill_col1:

        st.subheader(
            "✅ Matching Skills"
        )

        matching_skills = result[
            "matching_skills"
        ]

        if matching_skills:

            for skill in matching_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.write(
                "No matching skills detected."
            )


    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------

    with skill_col2:

        st.subheader(
            "❌ Missing Skills"
        )

        missing_skills = result[
            "missing_skills"
        ]

        if missing_skills:

            for skill in missing_skills:

                st.warning(
                    f"• {skill}"
                )

        else:

            st.success(
                "No missing technical skills detected."
            )


    # =====================================================
    # KEYWORDS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🔑 Important Job Keywords'
        '</div>',
        unsafe_allow_html=True
    )

    keywords = result[
        "keywords"
    ]

    if keywords:

        for keyword in keywords:

            st.markdown(
                f'<span class="badge">{keyword}</span>',
                unsafe_allow_html=True
            )

    else:

        st.write(
            "No keywords detected."
        )


    # =====================================================
    # SUITABLE ROLES
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '💼 Suitable Roles'
        '</div>',
        unsafe_allow_html=True
    )

    suitable_roles = result[
        "suitable_roles"
    ]

    if suitable_roles:

        for role in suitable_roles:

            st.info(
                f"💼 {role}"
            )

    else:

        st.write(
            "No suitable roles identified."
        )


    # =====================================================
    # STRENGTHS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '💪 Resume Strengths'
        '</div>',
        unsafe_allow_html=True
    )

    strengths = result[
        "strengths"
    ]

    if strengths:

        for strength in strengths:

            st.success(
                f"✅ {strength}"
            )

    else:

        st.write(
            "No strengths identified."
        )


    # =====================================================
    # WEAKNESSES
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '⚠️ Resume Weaknesses'
        '</div>',
        unsafe_allow_html=True
    )

    weaknesses = result[
        "weaknesses"
    ]

    if weaknesses:

        for weakness in weaknesses:

            st.warning(
                f"⚠️ {weakness}"
            )

    else:

        st.write(
            "No major weaknesses identified."
        )


    # =====================================================
    # IMPROVEMENTS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🚀 How to Improve Your Resume'
        '</div>',
        unsafe_allow_html=True
    )

    improvements = result[
        "improvements"
    ]

    if improvements:

        for index, improvement in enumerate(
            improvements,
            start=1
        ):

            st.write(
                f"**{index}.** {improvement}"
            )

    else:

        st.write(
            "No improvement suggestions available."
        )


    # =====================================================
    # FINAL FEEDBACK
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📝 Final Feedback'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        result["final_feedback"]
    )


    # =====================================================
    # PDF REPORT
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📥 Download Your Report'
        '</div>',
        unsafe_allow_html=True
    )

    try:

        pdf_file = create_pdf_report(
            result
        )

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="AI_Resume_Analyzer_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"PDF report could not be generated: {e}"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AI Resume Analyzer • Python • Streamlit •
        PyMuPDF • Gemini • ReportLab
    </div>
    """,
    unsafe_allow_html=True
)