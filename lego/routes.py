# -----------------------------------------------------------------------------
# Routing for the application.
#
# This is essentially the controllers for the application in terms of MVC,
# but all in one.
# -----------------------------------------------------------------------------

from functools import cmp_to_key
import os

from flask import render_template, flash, redirect, request, url_for, g, abort
from flask_login import login_user, logout_user, current_user, login_required

from lego import app, db, lm
from lego.forms import LoginForm, ScoreRoundForm
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
    stage = 0

    if stage == 0:
        top = teams[:8]
        second = teams[8:16]
        third = teams[16:]

        return render_template('scoreboard_bristol.html', title='Scoreboard', round=True,
                               top_eight=top, second_eight=second, third_eight=third)

    # quarter finals
    if stage == 2:
        return render_template('scoreboard_bristol.html', title='Scoreboard - Quarter Final',
                               quarter_final=True, top_eight=teams)

    # semi final
    if stage == 3:
        return render_template('scoreboard_bristol.html', title='Scoreboard - Semi Final',
                               semi_final=True, top_eight=teams)

    # final
    if stage == 4:
        return render_template('scoreboard_bristol.html', title='Scoreboard - Final',
                               final=True, top_eight=teams)


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
        attempt = len(team.scored_attempts) + 1

        if attempt > 3:
            flash('Team has no more attempts remaining')
        else:
            if form.confirm.data == '1':
                flash('Submit')
                setattr(team, 'attempt_{!s}'.format(attempt), score)
                db.session.commit()

                flash('Submitted for team: {!s}, score: {!s}, attempt: {!s}' \
                      .format(team.name, score, attempt))

                return redirect(url_for('judges_score_round'))

            flash('Calculate')

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

            form.attempt.data = attempt

            return render_template('judges/score_round.html', title='Score round',
                                   form=form, confirm=True)

    return render_template('judges/score_round.html', title='Score round', form=form)


@app.route('/admin/')
@app.route('/admin/home')
@login_required
def admin_home():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Home'


@app.route('/admin/teams/')
@login_required
def admin_teams():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams'


@app.route('/admin/teams/new')
@login_required
def admin_teams_new():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/New'


@app.route('/admin/teams/edit')
@login_required
def admin_teams_edit():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/Edit'

@app.route('/admin/teams/score')
@login_required
def admins_teams_score():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/Score'


@app.route('/admin/teams/score/edit')
@login_required
def admins_teams_score():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/Score/Edit'


@app.route('/admin/teams/score/reset')
@login_required
def admins_teams_score():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/Score/Reset'
