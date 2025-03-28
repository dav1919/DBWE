import logging
from logging.handlers import SMTPHandler, RotatingFileHandler  # SMTPHandler entfernt
import os
from datetime import datetime  # Importiere datetime
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#from flask_mail import Mail  # Entfernt
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
#from elasticsearch import Elasticsearch  # Entfernt
#from redis import Redis # Entfernt
#import rq  # Entfernt
from config import Config

def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
#mail = Mail()  # Entfernt
moment = Moment()
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    #mail.init_app(app)  # Entfernt
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # Elasticsearch und Redis entfernt
    #app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    #    if app.config['ELASTICSEARCH_URL'] else None
    #app.redis = Redis.from_url(app.config['REDIS_URL'])
    #app.task_queue = rq.Queue('prokrastinie-tasks', connection=app.redis)


    # Blueprints (Fehler, Authentifizierung, Haupt-App)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    #from app.cli import bp as cli_bp #Keine Sprachdateien mehr benÃ¶tigt
    #app.register_blueprint(cli_bp)

    from app.api import bp as api_bp #Import here
    app.register_blueprint(api_bp, url_prefix='/api') #Register



    # Logging (ohne Mail-Versand)
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/prokrastinie.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('ProkrastiNie startup')
    @app.context_processor
    def inject_datetime():
        return dict(datetime=datetime)

    return app

from app import models