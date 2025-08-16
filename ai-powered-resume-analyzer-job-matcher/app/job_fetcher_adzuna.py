
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY')
BASE_URL = 'https://api.adzuna.com/v1/api/jobs/in/search/1'

def fetch_jobs_from_adzuna(query, num=30):
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page': num,
        'what': query,
        'content-type': 'application/json'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    jobs = []
    now = datetime.utcnow()
    for job in data.get('results', []):
        created = job.get('created')
        # Adzuna 'created' is ISO8601 string, e.g. '2023-08-15T10:00:00Z'
        if created:
            try:
                created_dt = datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
            except Exception:
                continue
            if (now - created_dt) > timedelta(days=7):
                continue
        jobs.append({
            'title': job.get('title'),
            'company': job.get('company', {}).get('display_name', ''),
            'description': job.get('description', ''),
            'link': job.get('redirect_url', ''),
            'location': job.get('location', {}).get('display_name', '')
        })
    return jobs
