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

    practice_team = Team(number=-1, name='Practice', is_practice=True)
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
    short_help='Add teams to the database from a file.',
    help='Add teams to the database from a file. The file should contain one team per line.')
@click.argument('file', type=click.File())
def add_teams(file):
    for line in file:
        line = line.strip()

        if not line:
            continue

        number, name = line.split(',', 2)
        name = name.strip()

        try:
            number = int(number.strip())
            assert number > 0
        except (ValueError, AssertionError):
            click.echo('Invalid number: {!s}'.format(number))
            return

        click.echo('Adding team: {!s} (number: {!s}).'.format(name, number))

        team = Team(number=number, name=name)
        db.session.add(team)

    db.session.commit()
    click.echo('Teams successfully added.')

@app.cli.command('reset-teams',
    short_help='Remove all teams from the database.')
def reset_teams():
    click.echo('All teams will be deleted from the database.')

    if click.confirm('Do you wish to continue?', abort=True):
        db.session.query(Team).delete()
        db.session.commit()
        click.echo('Teams deleted.')
