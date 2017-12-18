# -------------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------

import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# use a helpful error message here as it can be a bit confusing otherwise
try:
    import lego.config as config
except ImportError:
    logging.error('Could not import config module. Please ensure you have copied '
                  'config.sample.py to config.py as detailed in the setup instructions.')
    sys.exit(1)

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

# stage
def load_stage() -> int:
    try:
        cur_path = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(cur_path, 'tmp', '.stage')) as fh:
            stage = int(fh.read().strip())

        assert stage >= 0
        assert stage <= 3

    except IOError:
        logging.error('Could not open stag file. Please run "flask init" first.')
        return 0

    except (ValueError, AssertionError):
        logging.error('Invalid value found for stage. Please run "flask init" to correct this.')
        return 0

    return stage

app.load_stage = load_stage

# imports of modules that require app
from lego import cli
from lego import routes
from lego.models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
