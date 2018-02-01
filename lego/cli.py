# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from base64 import b64encode
import os

import click
from sqlalchemy import asc

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

    _set_stage()


def _request_password(user: str, default: str):
    pword = click.prompt('Enter password for {!s}'.format(user), hide_input=True, default=default)

    # allow them to use the default
    if pword == default:
        return default

    pword2 = click.prompt('Confirm password for {!s}'.format(user), hide_input=True)

    if pword != pword2:
        click.echo('Passwords do not match.')
        raise click.Abort()

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


@app.cli.command('list-teams',
    short_help='List all teams from the database.')
@click.option('--practice', is_flag=True, help='Include the practice team.')
@click.option('--active', is_flag=True, help='Don\'t show teams that aren\'t currently active.')
def list_teams(practice: bool, active: bool):
    filters = {}

    if practice:
        filters.update({'is_practice': True})

    if active:
        filters.update({'active': True})

    teams = Team.query.filter_by(**filters).order_by(asc('number')).all()

    click.echo('  Number   Name')
    click.echo(' -------- --------------')

    for t in teams:
        click.echo('  {:<6}   {!s}'.format(t.number, t.name))


@app.cli.command('stage', short_help='Set the current stage.')
def set_stage():
    _set_stage()


def _set_stage():
    stage_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp', '.stage')

    while True:
        stage = click.prompt('Enter stage (0-4)')

        try:
            stage = int(stage)
        except ValueError:
            click.echo('Invalid value for stage: {!s}'.format(stage))
            continue

        stages = ('round_1', 'round_2', 'quarter_final', 'semi_final', 'final')
        stage_txt = stages[stage]

        if app.config['LEGO_APP_TYPE'] == 'bristol' and stage == 1:
            click.echo('Round 2 is only available during UK final.\n'
                       'If this is not an error, please change your config.py and try again.')
            raise click.Abort()

        click.echo('You have chosen {!s} ({!s}).'.format(stage_txt, stage))

        if click.confirm('Is this correct?'):
            try:
                with open(stage_file_path, 'w') as fh:
                    fh.write(str(stage))
            except IOError as e:
                click.echo('Could not save stage to file. ({!s})'.format(e))
                raise click.Abort()

            click.echo('Successfully set stage.')
            return
