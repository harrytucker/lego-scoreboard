# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

import os.path as path

WTF_CSRF_ENABLED = True
SECRET_KEY = 'your-secret-key'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    path.join(path.dirname(path.abspath(__file__)), 'tmp', 'lego.db')
