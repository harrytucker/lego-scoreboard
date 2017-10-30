# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import render_template, flash, redirect, request, url_for, g, abort
from flask_login import login_user, logout_user, current_user, login_required

from . import app, lm
from .forms import tasks, LoginForm, ScoreRoundForm
from .models import User, Team

@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(403)
def page_not_found(error):
    return render_template('errors/403.html', title='Permission denied'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page not found'), 404


@app.errorhandler(500)
def internal_server_error(error):
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

        flash('Login requested: username={!s}, password={!s}' \
              .format(username, password))

        res = User.authenticate(username, password)

        if isinstance(res, User):
            flash('Logged in successfully')
            login_user(res)
            return redirect('/home')

        flash(res)

    return render_template('login.html', title='Log in', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html', title='Scoreboard',
                           qualifying=[], not_qualifying=[])


@app.route('/tasks')
def tasks():
    return render_template('tasks.html', title='Completed Tasks')


@app.route('/judges')
@app.route('/judges/home')
@login_required
def judges_home():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    return render_template('judges/home.html', title='Judges Home')


@app.route('/judges/scoreround')
@login_required
def judges_score_round():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    form = ScoreRoundForm()

    form.team.choices = [('', '--Select team--'), ('-1', 'PRACTICE')]
    form.team.choices += [(t.id, t.name) for t in Team.query.order_by('name')]

    flash(dir(tasks))
    flash(dir(tasks.__file__))
    task_forms = [f for f in dir(tasks) if not f.startswith('_') and f[:1].isupper()]
    form.task.choices = [('', '--Select task--')]

    for f in task_forms:
        form.task.choices.append((f.title, f.title))

    if form.validate_on_submit():
        team_id = request.form['team']
        team = Team.get(team_id)
        flash('team={!s}', team.name)

    return render_template('judges/scoreround.html', title='Score round', form=form)


@app.route('/judges/scoretask')
@login_required
def judges_score_task():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    # TODO

    return 'TODO'


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


@app.route('/admin/teams/<name>/edit')
@login_required
def admin_teams_edit():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/Edit'
