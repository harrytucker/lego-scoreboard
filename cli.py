# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from base64 import b64encode
import os

import click

from . import app, db
from .models import *

@app.cli.command('init', short_help='Initialise the application.',
    help='Initialise the application by creating the database and the default '
         'users - Admin and Judge.')
def init_app():
    click.echo('Initialising application...')
    db.create_all()
    click.echo('Database created.')

    admin = 'Admin'
    admin_pword = _request_password(admin)

    judge = 'Judge'
    judge_pword = _request_password(judge)

    admin_user = User(username=admin, password=admin_pword, is_admin=True)
    db.session.add(admin_user)
    judge_user = User(username=judge, password=judge_pword, is_judge=True)
    db.session.add(judge_user)

    db.session.commit()
    click.echo('Default users created.')


def _request_password(user: str):
    pword = click.prompt('Enter password for {!s}'.format(user), hide_input=True)
    pword2 = click.prompt('Confirm password for {!s}'.format(user), hide_input=True)

    if pword != pword2:
        raise click.Abort('Passwords do not match.')

    return pword


@app.cli.command('generate-secret-key',
    short_help='Generate a secret key to set in config.py.',
    help='Generate a secret key to set in config.py. The key is used to encrypt '
         'the session cookie to prevent session hijacking.')
def generate_secret_key():
    key = b64encode(os.urandom(64)).decode('utf-8')
    click.echo('Secret key: {!s}'.format(key))

