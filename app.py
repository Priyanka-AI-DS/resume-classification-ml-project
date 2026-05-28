# ============================== 
# SMART AI RECRUITER SYSTEM (DARK THEME FIXED)
# ==============================

import streamlit as st
import pickle
import re
import PyPDF2
import docx
import pytesseract
from PIL import Image
import tempfile

# OCR Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load model
model = pickle.load(open("final_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# PAGE CONFIG
st.set_page_config(page_title="Smart AI Recruiter", layout="centered")

# DARK UI CSS (FIXED WHITE BOX)
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

/* Background */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.80), rgba(0,0,0,0.80)),
                url("https://images.unsplash.com/photo-1551288049-bebda4e38f71");
    background-size: cover;
    background-position: center;
    font-family: 'Poppins', sans-serif;
}

/* Main Card */
.main-card {
    background: rgba(0, 0, 0, 0.65);
    padding: 35px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    max-width: 750px;
    margin: auto;
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 25px;
}

/* Labels */
label {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 600;
}

/* Inputs */
.stRadio div, .stSelectbox div {
    font-size: 16px !important;
    color: #ffffff !important;
}

/* Dropdown fix */
.stSelectbox div[data-baseweb="select"] {
    color: black !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(45deg, #0072ff, #00c6ff);
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #00c6ff;
    padding: 15px;
    border-radius: 12px;
    background: rgba(255,255,255,0.08);
    color: white;
}

/* 🔥 FIXED METRIC (NO WHITE BOX) */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08);  /* dark glass */
    padding: 20px;
    border-radius: 12px;
    color: white;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.2);
}

/* Success */
.stSuccess {
    font-size: 18px !important;
}

/* Error */
.stError {
    font-size: 18px !important;
}

</style>
""", unsafe_allow_html=True)

# FUNCTIONS
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

def extract_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t
    return text

def extract_docx(file):
    doc = docx.Document(file)
    return " ".join([p.text for p in doc.paragraphs])

def extract_ocr(file):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        image = Image.open(tmp.name)
        text = pytesseract.image_to_string(image)
    return text

# JOB ROLES
job_roles = {
    "Python Developer": ["python", "django", "flask", "api"],
    "Data Scientist": ["python", "machine learning", "pandas", "numpy"],
    "SQL Developer": ["sql", "database", "oracle"],
    "Workday Consultant": ["workday", "hcm", "integration"]
}

# UI START
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.markdown("<div class='title'>Smart AI Recruiter</div>", unsafe_allow_html=True)

mode = st.radio("Select Mode", ["📂 Category Prediction", "🎯 Job Shortlisting"])

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "png", "jpg"])

if uploaded_file:

    text = ""
    file_name = uploaded_file.name

    try:
        if file_name.endswith(".pdf"):
            text = extract_pdf(uploaded_file)
            if text.strip() == "":
                text = extract_ocr(uploaded_file)

        elif file_name.endswith(".docx"):
            text = extract_docx(uploaded_file)

        elif file_name.endswith((".png", ".jpg")):
            text = extract_ocr(uploaded_file)

        st.success("✅ Resume processed")

        if mode == "📂 Category Prediction":

            if st.button("Predict Category"):
                clean = clean_text(text)
                vector = tfidf.transform([clean])
                category = model.predict(vector)[0]

                st.success(f"📄 Category: {category}")

        else:
            selected_job = st.selectbox("Select Job Role", list(job_roles.keys()))

            if st.button("Analyze Resume"):

                clean = clean_text(text)
                vector = tfidf.transform([clean])
                category = model.predict(vector)[0]

                st.success(f"📄 Predicted Category: {category}")

                required_skills = job_roles[selected_job]
                matched = [skill for skill in required_skills if skill in clean]

                match_score = int((len(matched) / len(required_skills)) * 100)

                st.metric("📊 Match Score", f"{match_score}%")

                if match_score > 10:
                    st.success("## 🎯 Shortlisted ✅")
                else:
                    st.error("❌ Not Shortlisted")

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)