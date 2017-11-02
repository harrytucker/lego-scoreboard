# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import render_template, flash, redirect, request, url_for, g, abort
from flask_login import login_user, logout_user, current_user, login_required

from lego import app, lm
from lego.forms import LoginForm, ScoreRoundForm
from lego.forms.tasks import TASK_FORMS, form_to_template
from lego.models import User, Team, Practice


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
            return redirect(url_for('home'))

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


@app.route('/judges/scoreround', methods=['GET', 'POST'])
@login_required
def judges_score_round():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    form = ScoreRoundForm()

    form.team.choices = [('', '--Select team--'), ('-1', 'PRACTICE')]
    form.team.choices += [(t.id, t.name) for t in Team.query.order_by('name')]

    flash(form.task.choices)

    if form.validate_on_submit():
        team_id = int(request.form['team'])
        task_id = int(request.form['task'])

        # practice_mode
        if team_id == -1:
            team = Practice()
        else:
            team = Team.query.get(team_id)

        task_form = TASK_FORMS[task_id + 1]

        flash('team={!s}'.format(team.name))
        flash('task={!s}'.format(task_form.title))

        return redirect(url_for('judges_score_task', task=task_id, team=team.id))

    return render_template('judges/scoreround.html', title='Score round', form=form)


@app.route('/judges/scoretask', methods=['GET', 'POST'])
@login_required
def judges_score_task():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    team_id = request.args.get('team')
    task_id = request.args.get('task')

    # not enough info from score round
    if team_id is None:
        flash('Team not found')
        return redirect(url_for('judges_score_round'))

    if task_id is None:
        flash('Task not found')
        return redirect(url_for('judges_score_round'))

    # practice mode
    if team_id == '-1':
        flash('Pratice mode enabled')
        team = Practice()
    else:
        team = Team.query.get(team_id)

    # invalid team
    if team is None:
        flash('Team not found')
        return redirect(url_for('judges_score_round'))

    try:
        task_form = TASK_FORMS[int(task_id)](request.values)
        task_template = form_to_template(task_form)
        flash(task_template)
    except ValueError:
        flash('Task not found')
        return redirect(url_for('judges_score_round'))


    if task_form.validate_on_submit():
        flash('Successfully submitted')
        flash('Points scored: {0!s}'.format(task_form.points_scored()))

    return render_template('judges/tasks/{0!s}.html'.format(task_template), title='Score task',
                           form=task_form, team=team)


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
