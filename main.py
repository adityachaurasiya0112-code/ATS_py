import re
import streamlit as st
import PyPDF2

# Tokenizer (regex-based)
def simple_tokenizer(text):
    return re.findall(r'\b\w+\b', text.lower())

def clean_and_tokenize(text):
    return set(simple_tokenizer(text))

def compare_keywords(resume_text, job_desc_text):
    resume_words = clean_and_tokenize(resume_text)
    job_keywords = clean_and_tokenize(job_desc_text)

    matched_keywords = resume_words & job_keywords
    missing_keywords = job_keywords - resume_words
    score = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0

    return round(score, 2), matched_keywords, missing_keywords

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# --- Streamlit UI ---
st.set_page_config(page_title="ATS Resume Checker", layout="centered")
st.title("📄 ATS Resume Checker")

# Upload resume file
uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF or TXT)", type=["pdf", "txt"])

# Paste job description
job_input = st.text_area("🧾 Paste Job Description", height=200)

# Check button
if st.button("🔍 Check Match"):
    if not uploaded_file:
        st.warning("Please upload a resume file.")
    elif job_input.strip() == "":
        st.warning("Please paste a job description.")
    else:
        # Extract text from resume
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            resume_text = uploaded_file.read().decode("utf-8")
        else:
            st.error("Unsupported file format.")
            st.stop()

        # Run ATS matching
        score, matched, missing = compare_keywords(resume_text, job_input)

        # Show results
        st.success(f"✅ ATS Match Score: {score}%")

        with st.expander("✅ Matched Keywords"):
            st.write(", ".join(sorted(matched)) if matched else "None")

        with st.expander("❌ Missing Keywords"):
            st.write(", ".join(sorted(missing)) if missing else "None")
