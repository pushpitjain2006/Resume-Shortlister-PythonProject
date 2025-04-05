import streamlit as st
import time
from scorer import score_resume_with_jd
import fitz

st.set_page_config(page_title="Resume Shortlister", layout="centered")

st.title("AI Resume Shortlister")
st.markdown("Pushpit jain 23/SE/123"
            "Priyanshu Tripathi 23/SE/122")
st.markdown("Upload multiple resumes and a job description to get ranked matches.")


uploaded_files = st.file_uploader("📂 Upload multiple resumes (PDFs)", type=["pdf"], accept_multiple_files=True)
job_description = st.text_area("🧾 Paste Job Description Here", height=200)

def extract_text(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


if st.button("Shortlist Resumes"):
    if not uploaded_files or not job_description:
        st.error("Please upload resumes and paste the job description.")
    else:
        with st.spinner("Processing resumes..."):
            results = []

            for uploaded_file in uploaded_files:
                resume_text = extract_text(uploaded_file)
                feedback = score_resume_with_jd(resume_text, job_description)
                results.append((uploaded_file.name, feedback))
                time.sleep(0.5)

            results.sort(key=lambda x: x[1]["score"], reverse=True)
            st.success("Here are the ranked resumes:")

            for idx, (filename, data) in enumerate(results, 1):
                with st.expander(f"📄 {idx}. {filename} — Score: {data['score']}"):
                    st.markdown("### ✅ Strengths")
                    for strength in data.get("strengths", []):
                        st.markdown(f"- {strength}")

                    st.markdown("### ⚠️ Weaknesses")
                    for weakness in data.get("weaknesses", []):
                        st.markdown(f"- {weakness}")