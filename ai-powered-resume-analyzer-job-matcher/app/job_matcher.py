from sentence_transformers import SentenceTransformer, util
from .db import get_all_jobs
import numpy as np

model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Helper to highlight keywords
from collections import defaultdict

def get_job_matches(resume_text, jobs=None):
    if jobs is None:
        jobs = get_all_jobs()
    resume_emb = model.encode([resume_text])[0]
    matches = []
    highlights = defaultdict(dict)
    import re
    from collections import Counter
    def extract_keywords(text, top_n=10):
        # Simple keyword extraction: most common nouns/words > 3 chars
        words = re.findall(r'\b\w{4,}\b', text.lower())
        stopwords = set(['with','from','that','this','have','will','your','about','using','such','their','which','should','also','other','more','than','must','able','work','team','role','good','well','skills','required','requirements','preferred','experience','knowledge','strong','excellent','ability','etc','and','for','the','you','are','our','who','job','per','all','any','can','but','not','get','out','use','has','its','was','his','her','she','him','they','them','been','had','were','what','when','where','how','why','while','each','few','own','same','so','too','very','s','t','just','now','d','ll','m','o','re','ve','y','ain','aren','couldn','didn','doesn','hadn','hasn','haven','isn','ma','mightn','mustn','needn','shan','shouldn','wasn','weren','won','wouldn'])
        filtered = [w for w in words if w not in stopwords]
        most_common = [w for w, _ in Counter(filtered).most_common(top_n)]
        return most_common
    for idx, job in enumerate(jobs):
        job_emb = model.encode([job.description])[0]
        score = float(util.cos_sim(resume_emb, job_emb))
        # If job.skills attribute exists, use it; else, extract from description
        if hasattr(job, 'skills') and job.skills:
            job_skills = [s.strip().lower() for s in job.skills.split(',')]
        else:
            job_skills = extract_keywords(job.description)
        resume_text_lower = resume_text.lower()
        missing = [s for s in job_skills if s and s not in resume_text_lower]
        present = [s for s in job_skills if s and s in resume_text_lower]
        matches.append({
            'title': job.title,
            'description': job.description,
            'score': round(score*100, 2),
            'missing': missing,
            'present': present
        })
        # Use idx as fallback key if job has no id
        highlights[getattr(job, 'id', idx)] = {'missing': missing, 'present': present}
    matches = sorted(matches, key=lambda x: x['score'], reverse=True)
    return matches, highlights

def get_resume_suggestions(resume_text, matches):
    # For demo: just save a PDF with missing keywords for top match
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    filename = 'suggestions.pdf'
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Resume Improvement Suggestions:")
    if matches:
        top = matches[0]
        c.drawString(100, 730, f"Job: {top['title']}")
        c.drawString(100, 710, "Missing Keywords:")
        y = 690
        for kw in top['missing']:
            c.drawString(120, y, f"- {kw}")
            y -= 20
    c.save()
    return filename
