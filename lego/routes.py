# -----------------------------------------------------------------------------
# Routing for the application.
#
# This is essentially the controllers for the application in terms of MVC,
# but all in one.
# -----------------------------------------------------------------------------

from functools import cmp_to_key
import os
import re
import unicodedata

from flask import render_template, flash, redirect, request, url_for, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

from lego import app, db, lm
from lego.forms import LoginForm, ScoreRoundForm, EditTeamForm, StageForm
from lego.models import User, Team


@app.before_request
def before_request():
    g.user = current_user


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    """Append a cache buster to static assets.

    Based on: <http://flask.pocoo.org/snippets/40/>
    """
    if endpoint == 'static':
        filename = values.get('filename', None)

        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)

    return url_for(endpoint, **values)


@app.after_request
def after_request(response):
    app.logger.info('%s %s %s %s %s',
                    request.remote_addr,
                    request.method,
                    request.scheme,
                    request.full_path,
                    response.status)
    return response


@app.template_filter('slugify')
def slugify(value: str):
    """Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Based on: <https://gist.github.com/berlotto/6295018>.
    """
    if not value:
        return ''

    strip_re = re.compile(r'[^\w\s-]')
    hyphenate_re = re.compile(r'[-\s]+')

    app.logger.info('[slugify] value: %s (%s)', str(value), type(value))
    normalised_value = str(unicodedata.normalize('NFKD', value))
    app.logger.info('[slugify] normalised value: %s (%s)', str(normalised_value), type(normalised_value))
    strip_value = strip_re.sub('', str(normalised_value)).strip().lower()
    app.logger.info('[slugify] strip value: %s (%s)', str(strip_value), type(strip_value))
    hyphenate_value = hyphenate_re.sub('-', strip_value)

    return hyphenate_value


@app.errorhandler(403)
def page_not_found(error):
    return render_template('errors/403.html', title='Permission denied'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page not found'), 404


@app.errorhandler(Exception)
def internal_server_error(exc):
    app.logger.exception(exc)
    return render_template('errors/500.html', title='Internal error'), 500


@app.route('/')
@app.route('/home')
def home():
    teams = Team.query.all()
    return render_template('home.html', title='Home', teams=teams)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        res = User.authenticate(username, password)

        if isinstance(res, User):
            login_user(res)
            return redirect(url_for('home'))

        flash(res)

    return render_template('login.html', title='Log in', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/scoreboard')
def scoreboard():
    teams = Team.query.filter_by(active=True, is_practice=False).all()

    def compare(team_1, team_2):
        if team_1.highest_score > team_2.highest_score:
            return -1

        if team_1.highest_score < team_2.highest_score:
            return 1

        return 0

    teams = sorted(teams, key=cmp_to_key(compare))
    stage = app.load_stage()

    # TODO: swap the below with this
    # if app.config['LEGO_APP_TYPE'] in ('bristol', 'uk'):
    #     template = 'scoreboard_{!s}.html'.format(app.config['LEGO_APP_TYPE'])

    if app.config['LEGO_APP_TYPE'] == 'bristol':
        template = 'scoreboard_bristol.html'
    else:
        raise Exception('Unsupported value for LEGO_APP_TYPE: {!s}' \
                        .format(app.config['LEGO_APP_TYPE']))

    if stage == 0:
        top = teams[:8]
        second = teams[8:16]
        third = teams[16:]

        return render_template('scoreboard_bristol.html', title='Scoreboard', round=True,
                               first=top, second=second, third=third)

    # quarter finals
    if stage == 1:
        return render_template('scoreboard_bristol.html', title='Scoreboard - Quarter Final',
                               quarter_final=True, first=teams)

    # semi final
    if stage == 2:
        return render_template('scoreboard_bristol.html', title='Scoreboard - Semi Final',
                               semi_final=True, first=teams)

    # final
    if stage == 3:
        return render_template('scoreboard_bristol.html', title='Scoreboard - Final',
                               final=True, first=teams)


@app.route('/judges/score_round', methods=['GET', 'POST'])
@login_required
def judges_score_round():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    form = ScoreRoundForm()

    teams = Team.query.filter_by(active=True).order_by('id')
    form.team.choices = [('', '--Select team--')]
    form.team.choices += [(str(t.id), t.name) for t in teams]

    if form.validate_on_submit():
        team_id = form.team.data
        team = Team.query.get(team_id)
        score = form.points_scored()

        if form.confirm.data == '1':
            try:
                team.set_score(score)
            except Exception as exc:
                flash(str(exc))
            else:
                db.session.commit()

                flash('Submitted for team: {!s}, score: {!s}.' \
                      .format(team.name, score))

                return redirect(url_for('judges_score_round'))

        # don't set confirm in the form if this is a practice attempt
        if team.is_practice:
            flash('Practice attempt')
        else:
            form.confirm.data = '1'

        flash('Score: {!s}'.format(score))

        # data submitted to the form overrides whatever we set as data here
        # so we have to override that if something changed after the
        # initial confirmation
        if form.score.raw_data:
            form.score.raw_data[0] = score
        else:
            form.score.data = score

        return render_template('judges/score_round.html', title='Score round',
                               form=form, confirm=True)

    return render_template('judges/score_round.html', title='Score round', form=form)

@app.route('/admin/team')
@login_required
def admin_team():
    if not current_user.is_admin:
        return abort(403)

    teams = Team.query.filter_by(is_practice=False).order_by(Team.id)

    return render_template('admin/team.html', title='Teams', teams=teams)


@app.route('/admin/team/new', methods=['GET', 'POST'])
@login_required
def admin_team_new():
    if not current_user.is_admin:
        return abort(403)

    return render_template('admin/team_new.html', title='Add New Team')


@app.route('/admin/team/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_team_edit(id: int):
    if not current_user.is_admin:
        return abort(403)

    team = Team.query.filter_by(id=id).first()
    form = EditTeamForm()

    if form.validate_on_submit():
        try:
            team.number = form.number.data
            team.name = form.name.data
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('The name or number requested is already in use. Please use another one.')
        except Exception as e:
            db.session.rollback()
            flash('An unknown error occurred. See the error logs for more information.')
        else:
            flash('Team details successfully updated')
            return redirect(url_for('admin_team'))


    form.id.data = team.id
    form.name.data = team.name
    form.number.data = team.number

    return render_template('admin/team_edit.html', title='Edit Team', form=form)


@app.route('/admin/team/<int:id>/score/edit', methods=['GET', 'POST'])
@login_required
def admin_team_score_edit(id: int):
    if not current_user.is_admin:
        return abort(403)

    return render_template('admin/team_score_edit.html', title='Edit a Team Score')


@app.route('/admin/team/<int:id>/score/reset', methods=['GET', 'POST'])
@login_required
def admin_team_score_reset(id: int):
    if not current_user.is_admin:
        return abort(403)

    return render_template('admin/team_score_reset.html', title='Reset a Team Score')


@app.route('/admin/stage', methods=['GET', 'POST'])
def admin_stage():
    if not current_user.is_admin:
        return abort(403)

    stages = ('First Round', 'Quarter Final', 'Semi Final', 'Final')

    stage = app.load_stage()
    current_stage = stages[stage]

    form = StageForm()

    if form.validate_on_submit():
        new_stage = int(form.stage.data)
        cur_file_path = os.path.dirname(os.path.abspath(__file__))

        if new_stage <= stage:
            flash('Unable to go back a stage.')
        else:
            set_active_teams(new_stage)

            with open(os.path.join(cur_file_path, 'tmp', '.stage'), 'w') as fh:
                fh.write(str(new_stage))

            flash('Stage updated to: {!s}'.format(stages[int(new_stage)]))
            return redirect(url_for('admin_stage'))

    return render_template('admin/stage.html', title='Manage Stage', form=form,
                           current_stage=current_stage)


def set_active_teams(stage):
    def compare(team_1, team_2):
        if team_1.highest_score > team_2.highest_score:
            return -1

        if team_1.highest_score < team_2.highest_score:
            return 1

        return 0

    teams = Team.query.filter_by(active=True, is_practice=False).all()
    teams = sorted(teams, key=cmp_to_key(compare))

    if app.config['LEGO_APP_TYPE'] == 'bristol':
        for i, team in enumerate(teams):
            if stage == 1 and i >= 6:
                team.active = False

            if stage == 2 and i >= 4:
                team.active = False

            if stage == 3 and i >= 2:
                team.active = False

    elif app.config['LEGO_APP_TYPE'] == 'uk':
        for i, team in enumerate(teams):
            if stage == 1 and i >= 8:
                team.active = False

            if stage == 2 and i >= 4:
                team.active = False

            if stage == 3 and i >= 2:
                team.active = False

    db.session.commit()
