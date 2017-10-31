# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import lego.config as config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from lego import cli
from lego import routes
from lego.models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
