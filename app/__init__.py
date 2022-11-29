from flask import Flask
from flask_session import Session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from redis import Redis
import rq

# def create_app(config_class=Config):
app = Flask(__name__)
app.config.from_object(Config)
app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
session = Session(app)
login = LoginManager(app)
session.init_app(app)
bootstrap = Bootstrap(app)

from app import routes, models, error

