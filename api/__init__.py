from flask_api import FlaskAPI
from flask_mail import Mail
import os
from flask_cors import CORS


from instance.config import app_config
from api.base_model import db

mail = Mail()


def create_app(config_name):

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    "get develoments settings from the env variable"
    db.init_app(app)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'hcravens25@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ravens2018'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'hcravens25@gmail.com'
    mail.init_app(app)

    from api.business.views import biz
    from api.users.views import auth
    app.register_blueprint(biz)
    app.register_blueprint(auth)
    CORS(app)
    return app


"get develoments settings from the env variable"
config_name = os.getenv('APP_SETTINGS')

app = create_app(config_name)

