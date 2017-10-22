# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from base64 import b64encode
import os

import click

from . import app, db
from .models import *

@app.cli.command('init', short_help='Initialise the application.',
    help='Initialise the application.')
def init_app():
    click.echo('Initialising application...')
    db.create_all()
    click.echo('Database created.')


@app.cli.command('generate-secret-key',
    short_help='Generate a secret key to set in config.py.',
    help='Generate a secret key to set in config.py. The key is used to encrypt '
         'the session cookie to prevent session hijacking.')
def generate_secret_key():
    key = b64encode(os.urandom(64)).decode('utf-8')
    click.echo('Secret key: {!s}'.format(key))

