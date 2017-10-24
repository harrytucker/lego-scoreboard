# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import render_template, flash, redirect, request, url_for, g, abort
from flask_login import login_user, logout_user, current_user, login_required

from . import app, lm
from .forms import LoginForm
from .models import User, Team

@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Page not found'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', title='Internal error'), 500


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
    return 'Scoreboard'


@app.route('/tasks')
def tasks():
    return 'Tasks'


@app.route('/judges')
@app.route('/judges/home')
@login_required
def judges_home():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(404)

    return 'Judges/Home'


@app.route('/judges/scoreround')
@login_required
def judges_score_round():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(404)

    return 'Judges/Score Round'


@app.route('/admin/')
@app.route('/admin/home')
@login_required
def admin_home():
    if not current_user.is_admin:
        return abort(404)

    return 'Admin/Home'


@app.route('/admin/teams/')
@login_required
def admin_teams():
    if not current_user.is_admin:
        return abort(404)

    return 'Admin/Teams'


@app.route('/admin/teams/new')
@login_required
def admin_teams_new():
    if not current_user.is_admin:
        return abort(404)

    return 'Admin/Teams/New'


@app.route('/admin/teams/<name>/edit')
@login_required
def admin_teams_edit():
    if not current_user.is_admin:
        return abort(404)

    return 'Admin/Teams/Edit'
