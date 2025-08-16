import pdfplumber
import docx2txt

def parse_resume(filepath):
    if filepath.lower().endswith('.pdf'):
        with pdfplumber.open(filepath) as pdf:
            text = " ".join(page.extract_text() or '' for page in pdf.pages)
    elif filepath.lower().endswith('.docx'):
        text = docx2txt.process(filepath)
    elif filepath.lower().endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = ''
    return text
