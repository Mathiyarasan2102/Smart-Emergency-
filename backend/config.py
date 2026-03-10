import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_student_project_key'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_URI = os.path.join(BASE_DIR, 'database', 'blood_bank.db')
