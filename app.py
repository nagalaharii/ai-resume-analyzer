import json
import os

import streamlit as st
from google import genai
from google.genai import types

# ---------- 1. Page setup ----------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI Resume Analyzer")
st.write("Paste your resume and a job description to see how well they match.")

# Model name is kept here so it is easy to change later.
MODEL_NAME = "gemini-3-flash-preview"

# ---------- 2. API client ----------
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("API key not found. Add GEMINI_API_KEY to .streamlit/secrets.toml")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------- 3. Inputs ----------
resume_text = st.text_area("Your resume (paste text)", height=250)
job_description = st.text_area("Job description (paste text)", height=250)

# ---------- 4. Prompt ----------
def build_prompt(resume, job):
    return f"""You are an experienced HR recruiter.
Compare the resume with the job description below.

Return ONLY valid JSON in exactly this format, with no extra text:
{{
  "match_score": <number from 0 to 100>,
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "tips": ["tip1", "tip2", "tip3"]
}}

Rules:
- Base the score only on the resume and job description given.
- Give exactly 3 practical, specific tips.

RESUME:
{resume}

JOB DESCRIPTION:
{job}
"""


# ---------- 5. Call the AI ----------
def analyze(resume, job):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=build_prompt(resume, job),
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


# ---------- 6. Button and output ----------
if st.button("Analyze"):
    if not resume_text.strip() or not job_description.strip():
        st.warning("Please fill in both boxes.")
    else:
        with st.spinner("Analyzing..."):
            try:
                result = analyze(resume_text, job_description)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        st.subheader("Match Score")
        score = int(result["match_score"])
        st.metric("Score", f"{score} / 100")
        st.progress(score / 100)

        st.subheader("✅ Matching Skills")
        for skill in result["matching_skills"]:
            st.write(f"- {skill}")

        st.subheader("❌ Missing Skills")
        for skill in result["missing_skills"]:
            st.write(f"- {skill}")

        st.subheader("💡 Tips to Improve")
        for i, tip in enumerate(result["tips"], start=1):
            st.write(f"{i}. {tip}")

        st.caption("AI can make mistakes. Use this score as guidance, not a final decision.")