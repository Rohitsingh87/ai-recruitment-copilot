
import streamlit as st
import tempfile
from pathlib import Path

from src.pipeline import analyze_candidate

st.set_page_config(
    page_title="AI Recruitment Copilot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Recruitment Copilot")
st.write("Analyze resumes against job descriptions and generate interview questions.")

st.divider()

# Resume upload
st.subheader("1. Upload Resume")
uploaded_resume = st.file_uploader(
    "Upload a candidate's resume",
    type=["pdf"]
)

# Job description
st.subheader("2. Enter Job Description")
job_description = st.text_area(
    "Paste the complete job description here",
    height=250,
    placeholder="Paste the job title, required skills, responsibilities, and qualifications..."
)

# Analyze button
if st.button("Analyze Candidate", type="primary", use_container_width=True):

    if uploaded_resume is None:
        st.error("Please upload a resume PDF.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        temp_path = None

        try:
            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:
                temp_file.write(uploaded_resume.getvalue())
                temp_path = Path(temp_file.name)

            with st.spinner("Analyzing resume and job description..."):
                report = analyze_candidate(
                    str(temp_path),
                    job_description
                )

            st.success("Analysis completed successfully!")

            # Candidate information
            st.header("Candidate Profile")
            col1, col2, col3 = st.columns(3)

            col1.metric("Candidate", report.candidate.full_name)
            col2.metric("Job Role", report.job.job_title)
            col3.metric(
                "Skill Match",
                f"{report.skill_match.match_percentage:.2f}%"
            )

            st.write("**Email:**", report.candidate.email or "Not available")
            st.write("**Phone:**", report.candidate.phone or "Not available")

            # Education
            st.subheader("Education")
            if report.candidate.education:
                st.dataframe(
                    [
                        education.model_dump()
                        for education in report.candidate.education
                    ],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No education details extracted.")

            # Skills
            st.header("Skill Match Analysis")

            matched_col, missing_col, additional_col = st.columns(3)

            with matched_col:
                st.subheader("✅ Matched Skills")
                if report.skill_match.matched_skills:
                    for skill in report.skill_match.matched_skills:
                        st.write(f"• {skill}")
                else:
                    st.write("No matched skills.")

            with missing_col:
                st.subheader("❌ Missing Skills")
                if report.skill_match.missing_skills:
                    for skill in report.skill_match.missing_skills:
                        st.write(f"• {skill}")
                else:
                    st.write("No missing skills.")

            with additional_col:
                st.subheader("➕ Additional Skills")
                if report.skill_match.additional_skills:
                    for skill in report.skill_match.additional_skills:
                        st.write(f"• {skill}")
                else:
                    st.write("No additional skills.")

            # Summary and recommendations
            st.header("Recruitment Summary")
            st.write(report.summary)

            if report.recommendations:
                st.subheader("Recommendations")
                for recommendation in report.recommendations:
                    st.write(f"• {recommendation}")

            # Interview questions
            st.header("Generated Interview Questions")

            for index, question in enumerate(
                report.interview_questions,
                start=1
            ):
                with st.expander(
                    f"{index}. {question.question}"
                ):
                    st.write(f"**Category:** {question.category}")
                    st.write(f"**Difficulty:** {question.difficulty}")

                    if question.expected_topics:
                        st.write("**Expected topics:**")
                        for topic in question.expected_topics:
                            st.write(f"• {topic}")

            # Download report
            report_json = report.model_dump_json(indent=2)

            st.download_button(
                label="Download Analysis Report (JSON)",
                data=report_json,
                file_name="recruitment_analysis.json",
                mime="application/json"
            )

        except Exception as error:
            st.error("Analysis failed. Please check the inputs and try again.")
            st.exception(error)

        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink()
