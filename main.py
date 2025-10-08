import streamlit as st
import requests
import json
import io

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

st.set_page_config(page_title="AI Resume Builder & Analyzer", page_icon="💼", layout="centered")

st.title("💼 AI Resume Builder & Analyzer")
st.write("Enhance, rewrite, and analyze your resume using RapidAPI's AI Resume Builder API.")

tab1, tab2, tab3 = st.tabs(["📄 Upload or Paste Resume", "🤖 AI Resume Rewriter", "📊 Insights"])

resume_text = ""

with tab1:
    st.subheader("Upload or Paste Your Resume")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            if PyPDF2:
                reader = PyPDF2.PdfReader(uploaded_file)
                resume_text = "\n".join([page.extract_text() for page in reader.pages])
            else:
                st.error("PyPDF2 is not installed. Please install it to use PDF upload feature.")
        else:
            resume_text = uploaded_file.read().decode("utf-8")
    resume_text = st.text_area("Or paste your resume here:", resume_text, height=300)

with tab2:
    st.subheader("Rewrite Resume with AI ✨")
    if st.button("Rewrite Resume"):
        if not resume_text.strip():
            st.warning("Please upload or paste your resume first.")
        else:
            try:
                with st.spinner("Rewriting your resume with AI..."):
                    url = "https://ai-resume-builder-cv-checker-resume-rewriter-api.p.rapidapi.com/generateResume?noqueue=1&language=en"
                    headers = {
                        "x-rapidapi-key": "6d5a1ea9cdmsh0b7c5c815ef5aa4p14fe2djsnfa9b5a5d0f6d",
                        "x-rapidapi-host": "ai-resume-builder-cv-checker-resume-rewriter-api.p.rapidapi.com",
                        "Content-Type": "application/json",
                        "x-usiapps-req": "true"
                    }
                    payload = {"resumeText": resume_text}
                    response = requests.post(url, headers=headers, data=json.dumps(payload))

                    if response.status_code == 200:
                        data = response.json()
                        rewritten_resume = data.get("text", json.dumps(data, indent=2))
                        st.success("✅ Resume rewritten successfully!")
                        st.text_area("AI-Rewritten Resume:", rewritten_resume, height=400)
                        st.download_button("📥 Download Rewritten Resume", rewritten_resume, file_name="rewritten_resume.txt")
                        st.session_state["original_resume"] = resume_text
                        st.session_state["rewritten_resume"] = rewritten_resume
                    else:
                        st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

with tab3:
    st.subheader("📊 Resume Insights")
    if "original_resume" in st.session_state and "rewritten_resume" in st.session_state:
        orig = st.session_state["original_resume"]
        rew = st.session_state["rewritten_resume"]
        orig_len = len(orig.split())
        rew_len = len(rew.split())
        orig_chars = len(orig)
        rew_chars = len(rew)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Resume", f"{orig_len} words", f"{orig_chars} chars")
        with col2:
            st.metric("Rewritten Resume", f"{rew_len} words", f"{rew_chars} chars")

        improvement = ((rew_len - orig_len) / orig_len) * 100 if orig_len > 0 else 0
        st.write(f"**Content Expansion:** {improvement:.2f}%")
    else:
        st.info("Please rewrite a resume first to view insights.")
