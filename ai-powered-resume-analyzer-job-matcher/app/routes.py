from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash
from .resume_parser import parse_resume
from .nlp_utils import extract_entities
from .job_matcher import get_job_matches, get_resume_suggestions
from .db import get_all_jobs, add_resume
from .job_fetcher_adzuna import fetch_jobs_from_adzuna
import os

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('resume')
        if not file:
            flash('No file uploaded!', 'danger')
            return redirect(url_for('main.index'))
        filename = file.filename
        filepath = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(filepath)
        text = parse_resume(filepath)
        entities = extract_entities(text)
        add_resume(filename, text, entities)
        # Use top 2-3 skills as the job search query
        skill_query = ' '.join(entities.get('skills', [])[:3]) if entities.get('skills') else 'developer'
        adzuna_jobs = fetch_jobs_from_adzuna(query=skill_query, num=30)
        class JobObj:
            def __init__(self, title, description, link=None, skills=None):
                self.title = title
                self.description = description
                self.link = link
                self.skills = skills or ''
        jobs_for_matching = [JobObj(j['title'], j['description'] or '', j.get('link', ''), '') for j in adzuna_jobs]
        from . import job_matcher
        matches, highlights = job_matcher.get_job_matches(text, jobs=jobs_for_matching)
        for i, m in enumerate(matches):
            m['link'] = jobs_for_matching[i].link if i < len(jobs_for_matching) else ''
        suggestions_pdf = get_resume_suggestions(text, matches)
        return render_template('results.html', matches=matches, highlights=highlights, suggestions_pdf=suggestions_pdf)
    return render_template('index.html')

@main.route('/download_suggestions')
def download_suggestions():
    return send_file(os.path.join(os.getcwd(), 'suggestions.pdf'), as_attachment=True)

@main.route('/debug_jobs')
def debug_jobs():
    jobs = get_all_jobs()
    return "<br>".join([f"{job.title}: {job.skills}" for job in jobs])
