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

    .main-title {
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .score-card {
        padding: 20px;
        border-radius: 14px;
        background: #f8f9fa;
        border: 1px solid #e5e7eb;
        text-align: center;
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
    'Analyze your resume against a job description and discover how to improve your ATS compatibility.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Settings")

demo_mode = st.sidebar.toggle(
    "Demo / Local Mode",
    value=True
)

if demo_mode:

    st.sidebar.success(
        "Local analysis is enabled."
    )

    st.sidebar.caption(
        "No Gemini API call is required."
    )

else:

    st.sidebar.warning(
        "AI Mode uses the Gemini API."
    )

    st.sidebar.caption(
        "If your API quota is unavailable, switch back to Demo / Local Mode."
    )


st.sidebar.markdown("---")

st.sidebar.subheader("📌 How it works")

st.sidebar.write(
    "1. Upload your resume"
)

st.sidebar.write(
    "2. Paste a job description"
)

st.sidebar.write(
    "3. Analyze the resume"
)

st.sidebar.write(
    "4. Review ATS compatibility"
)

st.sidebar.write(
    "5. Download your report"
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
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )


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
    # EXTRACT RESUME
    # -----------------------------------------------------

    with st.spinner(
        "📖 Reading your resume..."
    ):

        try:

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        except Exception as e:

            st.error(
                f"Could not read the PDF: {e}"
            )

            st.stop()


    if not resume_text.strip():

        st.error(
            "No readable text was found in the uploaded PDF."
        )

        st.stop()


    # -----------------------------------------------------
    # ANALYZE
    # -----------------------------------------------------

    with st.spinner(
        "🤖 Analyzing your resume..."
    ):

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
                str(e)
            )

            st.stop()


    # =====================================================
    # SUCCESS
    # =====================================================

    st.success(
        "✅ Resume analysis completed successfully!"
    )


    # =====================================================
    # ATS COMPATIBILITY
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 ATS Compatibility</div>',
        unsafe_allow_html=True
    )


    ats_score = result["ats_score"]


    st.metric(
        "Overall ATS Score",
        f"{ats_score}/100"
    )


    st.progress(
        ats_score / 100
    )


    if ats_score >= 80:

        st.success(
            "Your resume has strong compatibility with this job description."
        )

    elif ats_score >= 60:

        st.info(
            "Your resume has moderate compatibility. "
            "Review the missing skills and keywords."
        )

    else:

        st.warning(
            "Your resume has lower compatibility. "
            "Review the missing skills, keywords and job requirements."
        )


    # =====================================================
    # DETAILED SCORES
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Detailed Scores</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🎯 Job Match",
            f"{result['job_match_score']}/100"
        )


    with col2:

        st.metric(
            "🔑 Keyword Match",
            f"{result['keyword_score']}/100"
        )


    with col3:

        st.metric(
            "🧠 Skills Match",
            f"{result['skills_score']}/100"
        )


    col4, col5, col6 = st.columns(3)


    with col4:

        st.metric(
            "📄 Resume Quality",
            f"{result['resume_quality_score']}/100"
        )


    with col5:

        st.metric(
            "💼 Experience",
            f"{result['experience_score']}/100"
        )


    with col6:

        st.metric(
            "📝 Resume Length",
            f"{len(resume_text.split())} words"
        )


    # =====================================================
    # SIMPLE SCORE BARS
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Score Comparison</div>',
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
            f"**{label}: {score}/100**"
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


        if job_analysis[
            "detected_skills"
        ]:

            for skill in job_analysis[
                "detected_skills"
            ]:

                st.write(
                    f"• {skill}"
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


        if job_analysis[
            "soft_skills"
        ]:

            for skill in job_analysis[
                "soft_skills"
            ]:

                st.write(
                    f"• {skill}"
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


        if job_analysis[
            "experience_requirements"
        ]:

            for item in job_analysis[
                "experience_requirements"
            ]:

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


        if job_analysis[
            "education_requirements"
        ]:

            for item in job_analysis[
                "education_requirements"
            ]:

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
        '<div class="section-title">'
        '🧠 Skill Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    skill_col1, skill_col2 = st.columns(2)


    with skill_col1:

        st.subheader(
            "✅ Matching Skills"
        )


        if result[
            "matching_skills"
        ]:

            for skill in result[
                "matching_skills"
            ]:

                st.success(
                    skill
                )

        else:

            st.write(
                "No matching skills detected."
            )


    with skill_col2:

        st.subheader(
            "❌ Missing Skills"
        )


        if result[
            "missing_skills"
        ]:

            for skill in result[
                "missing_skills"
            ]:

                st.warning(
                    skill
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


    if result[
        "keywords"
    ]:

        st.write(
            ", ".join(
                result[
                    "keywords"
                ]
            )
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


    for role in result[
        "suitable_roles"
    ]:

        st.info(
            f"💼 {role}"
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


    for strength in result[
        "strengths"
    ]:

        st.success(
            f"✅ {strength}"
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


    for weakness in result[
        "weaknesses"
    ]:

        st.warning(
            f"⚠️ {weakness}"
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


    for index, improvement in enumerate(
        result["improvements"],
        start=1
    ):

        st.write(
            f"**{index}.** {improvement}"
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
    "---"
)

st.caption(
    "AI Resume Analyzer • Python • Streamlit • "
    "Gemini • PyMuPDF • ReportLab"
)