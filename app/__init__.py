# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Database और LoginManager initialize
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # 🔹 Basic Config
    app.config['SECRET_KEY'] = 'your-secret-key'  # इसे change कर सकते हो
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 🔹 Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # login route का नाम अगर है तो डालो
    
    # 🔹 Import models
    from app.models import User  # User model चाहिए जो Flask-Login compatible हो

    # 🔹 Flask-Login: user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # user fetch from DB

    # 🔹 Import and register routes
    from .routes import main
    app.register_blueprint(main)

    return app