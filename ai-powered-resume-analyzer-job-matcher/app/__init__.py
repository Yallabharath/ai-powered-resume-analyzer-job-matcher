from flask import Flask
from .routes import main
from .db import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../jobs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    init_db(app)
    app.register_blueprint(main)
    return app
