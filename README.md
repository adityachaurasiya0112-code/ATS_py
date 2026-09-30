# 📄 ATS Resume Checker

The **ATS Resume Checker** is a Streamlit-based web app that analyzes how well your resume matches a given job description.  
It extracts text from your uploaded resume (PDF or TXT), compares keywords with the job description, and provides an **ATS Match Score** — helping you optimize your resume for better chances in automated shortlisting systems.

---

## 🚀 Features

- 📤 Upload your resume (PDF or TXT format)
- 🧾 Paste or type your job description
- ⚡ Instantly get your **ATS Match Score**
- ✅ See **matched keywords**
- ❌ See **missing keywords**
- 💡 Helps improve resume relevancy for ATS and recruiters

---

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** — for the web interface
- **PyPDF2** — for PDF text extraction
- **Regex (re)** — for keyword tokenization and comparison

---

## 🧩 Folder Structure

ATS_py/
├── main.py
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚙️ Installation & Run Locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/ayu-haker/ATS_py.git
   cd ATS_py
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy code
streamlit run main.py
Open in your browser:

arduino
Copy code
http://localhost:8501
🌐 Deploy on Streamlit Cloud
Push all files (main.py, requirements.txt, README.md) to your GitHub repo.

Go to streamlit.io/cloud

Click “New App”

Set:

Repository: ayu-haker/ATS_py

Branch: main

Main file path: main.py

Click Deploy

✅ Done! Your ATS Resume Checker will be live at:

arduino
Copy code
https://your-app-name.streamlit.app
📊 Example Output
ATS Match Score: 78%

Matched Keywords: python, sql, data, analysis

Missing Keywords: machine learning, cloud, leadership

💡 Future Enhancements
Add keyword highlighting in resume text

Support for DOCX format

Smart keyword suggestions based on job role

Visual progress bar for ATS score

👨‍💻 Author
Ayush (ayu-haker)
💼 Passionate developer building smart, helpful tools for students and job seekers.
📧 Feel free to connect and contribute!

⭐ If you like this project, give it a star on GitHub! ⭐

yaml
Copy code

---

Would you like me to make it look **more stylish** (with badges, emojis, and colored headings like a professional GitHub profile)? I can make that version too 🌈# ATS_py

