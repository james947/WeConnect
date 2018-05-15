from flask_api import FlaskAPI
import os
from instance.config import app_config
from api.baseModel import db

def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    "get develoments settings from the env variable"
    # config_name = os.getenv('APP_SETTINGS')
    db.init_app(app)
    return app


"get develoments settings from the env variable"
config_name = os.getenv('APP_SETTINGS')

from api.business.views import biz
from api.users.views import auth
app = create_app(config_name)
app.register_blueprint(biz)
app.register_blueprint(auth)
