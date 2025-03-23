import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # Mail-bezogene Einstellungen entfernt
    ADMINS = ['your-email@example.com']  # Optional: für Fehlermeldungen
    LANGUAGES = ['en', 'de'] #de für deutsch
    #MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY') # Nicht mehr benötigt.
    #ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') # Nicht mehr benötigt.
    #REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'       # Nicht mehr benötigt.
    POSTS_PER_PAGE = 25  # Beibehalten, kann für Tasks verwendet werden.