import spacy
nlp = spacy.load('en_core_web_sm')

SKILL_KEYWORDS = [
    # Web Developer
    'html', 'css', 'javascript', 'react', 'bootstrap', 'mern stack', 'mongodb', 'express', 'node.js',
    'api integration', 'frontend', 'backend', 'full stack', 'responsive design', 'ui/ux', 'git',
    'google generative ai', 'chatbot', 'secure login', 'analytics tracking', 'geolocation', 'url shortener'
]

def extract_entities(text):
    doc = nlp(text)
    skills = [kw for kw in SKILL_KEYWORDS if kw.lower() in text.lower()]
    education = [ent.text for ent in doc.ents if ent.label_ == 'ORG' or ent.label_ == 'EDUCATION']
    certifications = [ent.text for ent in doc.ents if 'certified' in ent.text.lower() or 'certificate' in ent.text.lower()]
    experience = [sent.text for sent in doc.sents if 'experience' in sent.text.lower()]
    return {
        'skills': skills,
        'education': education,
        'certifications': certifications,
        'experience': experience
    }
