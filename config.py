# import os
# from app import app  # Import the app instance


# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/ongc_backup_database")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = "your_secret_key"
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
import os

class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/ongc_backup_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
