# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import lego.config as config

app = Flask(__name__)
app.config.from_object(config)

# logging
logging.basicConfig(level=logging.DEBUG)
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
log_size = 1 * 1024 * 1024 # 1MB
log_count = 5

debug_fh = RotatingFileHandler(os.path.join(log_dir, 'debug.log'), 'a', log_size, log_count)
debug_fh.setLevel(logging.DEBUG)

error_fh = RotatingFileHandler(os.path.join(log_dir, 'error.log'), 'a', log_size, log_count)
error_fh.setLevel(logging.ERROR)

formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s '
                              '[in %(pathname)s:%(lineno)d]')
debug_fh.setFormatter(formatter)
error_fh.setFormatter(formatter)

app.logger.addHandler(debug_fh)
app.logger.addHandler(error_fh)

app.logger.info('Initialising application')

# database
db = SQLAlchemy(app)

# login manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# imports of modules that require app
from lego import cli
from lego import routes
from lego.models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
