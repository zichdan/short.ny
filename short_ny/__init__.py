from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from os import path
from .extensions import db
from .models import User
from .auth.users import auth
from .routes import shortner

from dotenv import load_dotenv

from.routes import shortner
from .config import config_dict


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    db.init_app(app)

    
    load_dotenv()
    
        
    # cache = Cache(app)
    # limiter = Limiter(get_remote_address)

    # qr = qrcode.QRCode(
    #     version = 1,
    #     error_correction = qrcode.constants.ERROR_CORRECT_L,
    #     box_size = 5,
    #     border = 4
    # )
    
    
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    app.register_blueprint(shortner)
    app.register_blueprint(auth)
    

    with app.app_context():
        db.create_all()
        

    
    return app




# def create_app(config=config_dict['dev']):
#     app = Flask(__name__)
    
#     app.config.from_pyfile(config_file)

#     db.init_app(app)




#     app.register_blueprint(shortner)
    
#     return app




  










