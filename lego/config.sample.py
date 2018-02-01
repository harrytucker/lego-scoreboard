# -----------------------------------------------------------------------------
# Configuration for the Lego Challenge application.
# -----------------------------------------------------------------------------

import os.path as path

# Default settings - you should not need to alter these
WTF_CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    path.join(path.dirname(path.abspath(__file__)), 'tmp', 'lego.db')

# Generate using `flask generate-secret-key`
SECRET_KEY = 'your-secret-key'

# One of: bristol, uk
LEGO_APP_TYPE = 'bristol'
