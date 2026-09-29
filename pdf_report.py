from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO


def create_pdf_report(result):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    story = []

    # Title
    story.append(
        Paragraph(
            "AI Resume Analyzer Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    # ATS Score
    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {result['ats_score']}/100",
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # Sections
    sections = [
        ("Matching Skills", result["matching_skills"]),
        ("Missing Skills", result["missing_skills"]),
        ("Important Keywords", result["keywords"]),
        ("Suitable Job Roles", result["suitable_roles"]),
        ("Resume Strengths", result["strengths"]),
        ("Resume Weaknesses", result["weaknesses"]),
        ("Improvement Suggestions", result["improvements"]),
    ]

    for heading, items in sections:

        story.append(
            Paragraph(
                heading,
                heading_style
            )
        )

        story.append(Spacer(1, 8))

        if items:

            for item in items:

                story.append(
                    Paragraph(
                        f"• {item}",
                        normal_style
                    )
                )

                story.append(Spacer(1, 4))

        else:

            story.append(
                Paragraph(
                    "None identified.",
                    normal_style
                )
            )

        story.append(Spacer(1, 12))

    # Final Feedback
    story.append(
        Paragraph(
            "Final Feedback",
            heading_style
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            result["final_feedback"],
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated using AI Resume Analyzer",
            normal_style
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer