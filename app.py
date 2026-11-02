
import streamlit as st
import pandas as pd
import plotly.express as px

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from resume_matcher import calculate_match


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer")
st.write(
    "Analyze your resume, compare it with a job "
    "description, and discover missing skills."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose your resume (PDF)",
        type=["pdf"]
    )

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Enter job requirements and skills..."
    )

st.divider()

if st.button("🔍 Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.warning("Please upload your resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text.strip():
                st.error(
                    "Could not extract text. "
                    "Please use a text-based PDF."
                )
                st.stop()

            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_description)

            matched_skills = sorted(
                set(resume_skills) & set(job_skills)
            )

            missing_skills = sorted(
                set(job_skills) - set(resume_skills)
            )

            match_score = calculate_match(
                resume_text, job_description
            )

            if job_skills:
                skill_score = (
                    len(matched_skills) / len(job_skills)
                ) * 100
                overall_score = (
                    0.6 * skill_score + 0.4 * match_score
                )
            else:
                skill_score = 0
                overall_score = match_score

            overall_score = round(overall_score, 2)

            st.success("Resume analyzed successfully!")

            st.header("📊 Analysis Dashboard")

            m1, m2, m3, m4 = st.columns(4)

            m1.metric(
                "Overall Match",
                f"{overall_score:.1f}%"
            )
            m2.metric(
                "Text Similarity",
                f"{match_score:.1f}%"
            )
            m3.metric(
                "Matched Skills",
                len(matched_skills)
            )
            m4.metric(
                "Missing Skills",
                len(missing_skills)
            )

            st.progress(
                min(100, max(0, int(overall_score)))
            )

            st.caption(
                "The overall score is a heuristic: "
                "60% skill overlap and 40% text "
                "similarity when job skills are found."
            )

            st.divider()

            left, right = st.columns(2)

            with left:
                st.subheader("✅ Matched Skills")
                if matched_skills:
                    for skill in matched_skills:
                        st.success(skill)
                else:
                    st.info("No matching skills detected.")

            with right:
                st.subheader("❌ Missing Skills")
                if missing_skills:
                    for skill in missing_skills:
                        st.error(skill)
                else:
                    st.info(
                        "No missing skills detected "
                        "from the supported skill list."
                    )

            st.divider()

            st.subheader("📈 Skills Comparison")

            chart_data = pd.DataFrame({
                "Category": [
                    "Matched Skills",
                    "Missing Skills"
                ],
                "Count": [
                    len(matched_skills),
                    len(missing_skills)
                ]
            })

            if job_skills:
                fig = px.pie(
                    chart_data,
                    names="Category",
                    values="Count",
                    hole=0.45,
                    color="Category",
                    color_discrete_map={
                        "Matched Skills": "#16a34a",
                        "Missing Skills": "#ef4444"
                    }
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            else:
                st.info(
                    "No supported skills found in "
                    "the job description."
                )

            st.divider()

            st.subheader("💡 Resume Improvement Suggestions")

            if missing_skills:
                st.write(
                    "Consider learning these skills "
                    "if they are relevant to your role:"
                )

                for skill in missing_skills:
                    st.write(f"• {skill}")

            if match_score < 40:
                st.warning(
                    "Your resume has low text similarity "
                    "with the job description. Review "
                    "the role requirements."
                )
            elif match_score < 70:
                st.info(
                    "Your resume has moderate text "
                    "similarity. Highlight relevant "
                    "projects and experience."
                )
            else:
                st.success(
                    "Your resume has high text similarity "
                    "with the job description."
                )

            st.write(
                "Only add skills and achievements "
                "that you genuinely possess."
            )

            st.divider()

            with st.expander("📄 Extracted Resume Text"):
                st.text_area(
                    "Resume Content",
                    resume_text,
                    height=300
                )

        except Exception as e:
            st.error(f"Error analyzing resume: {e}")
