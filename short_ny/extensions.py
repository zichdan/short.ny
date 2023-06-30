from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
cache = Cache()
limiter = Limiter(get_remote_address)
login_manager = LoginManager()
migrate = Migrate()




