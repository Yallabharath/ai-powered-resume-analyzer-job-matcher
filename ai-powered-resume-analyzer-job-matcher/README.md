# AI-Powered Resume Analyzer & Job Matcher

AI-powered resume analyzer that extracts skills, education & experience from PDF/DOCX files. Uses semantic matching with Hugging Face Transformers to match resumes against job descriptions, highlights missing keywords & generates improvement suggestions. Flask web app with responsive Bootstrap UI.

## Features
- Upload PDF/DOCX/TXT resumes
- Extract skills, education, certifications, and work experience
- Store and match against job descriptions
- Semantic matching using Hugging Face Transformers
- Highlight missing and existing keywords
- Download improved resume suggestions

## Setup Instructions

1. **Clone the repository**
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Download spaCy model:**
   ```
   python -m spacy download en_core_web_sm
   ```
4. **Run the app:**
   ```
   python run.py
   ```
5. **Access the app:**
   Open your browser at http://127.0.0.1:5000

## Notes
- Modular, production-ready code
- Easily extendable backend API
- Responsive Bootstrap UI
