from flask import Flask

import os, qrcode
# from os import path

from .extensions import db, cache, limiter, login_manager, migrate
from .models import User

from .auth.users import auth
from .routes import shortner

from dotenv import load_dotenv

from.routes import shortner
from .config import config_dict

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    db.init_app(app)

    load_dotenv()
    
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config.update(
        UPLOAD_PATH = os.path.join(BASE_DIR, 'static', 'qr-codes')
    )
        
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)
        
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 5,
        border = 4
    )
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    app.register_blueprint(shortner)
    app.register_blueprint(auth)
    

    with app.app_context():
        db.create_all()
        

    return app






  










