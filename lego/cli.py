# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from base64 import b64encode
import os

import click

from lego import app, db
from lego.models import User, Team

@app.cli.command('init', short_help='Initialise the application.',
    help='Initialise the application by creating the database and the default '
         'users - Admin and Judge.')
def init_app():
    click.echo('Initialising application...')
    db.create_all()
    click.echo('Database created.')

    admin = 'Admin'
    admin_pword = _request_password(admin, default='admin')

    judge = 'Judge'
    judge_pword = _request_password(judge, default='judge')

    admin_user = User(username=admin, password=admin_pword, is_admin=True)
    db.session.add(admin_user)
    judge_user = User(username=judge, password=judge_pword, is_judge=True)
    db.session.add(judge_user)

    practice_team = Team(name='Practice', is_practice=True)
    db.session.add(practice_team)

    db.session.commit()
    click.echo('Default users created.')
    click.echo('Practice team created.')


def _request_password(user: str, default: str):
    pword = click.prompt('Enter password for {!s}'.format(user), hide_input=True, default=default)

    # allow them to use the default
    if pword == default:
        return default

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


@app.cli.command('add-teams',
    short_help='Add teams to the database from a file. The file should contain one team per line.')
@click.argument('file', type=click.File())
def add_teams(file):
    for line in file:
        team_name = line.strip()

        if not team_name:
            continue

        click.echo('Adding team: {!s}'.format(team_name))

        team = Team(name=team_name)
        db.session.add(team)

    db.session.commit()
    click.echo('Teams successfully added')
