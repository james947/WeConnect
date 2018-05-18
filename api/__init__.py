from flask_api import FlaskAPI
import os
from instance.config import app_config
from api.base_model import db


def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    "get develoments settings from the env variable"
    db.init_app(app)
    from api.business.views import biz
    from api.users.views import auth
    app.register_blueprint(biz)
    app.register_blueprint(auth)
    return app


"get develoments settings from the env variable"
config_name = os.getenv('APP_SETTINGS')

app = create_app(config_name)

