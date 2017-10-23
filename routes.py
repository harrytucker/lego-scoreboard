# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import render_template, flash, redirect, request, url_for, g
from flask_login import login_user, logout_user, current_user, login_required

from . import app, lm
from .forms import LoginForm
from .models import User, Team

@app.before_request
def before_request():
    g.user = current_user

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
        flash('Login requested: username=%s, password=%s',
              request.args.username, request.args.password)

        res = User.authenticate(request.args.username, request.args.password)

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
def judges_home():
    return 'Judges/Home'


@app.route('/judges/scoreround')
def judges_score_round():
    return 'Judges/Score Round'


@app.route('/admin/')
@app.route('/admin/home')
def admin_home():
    return 'Admin/Home'


@app.route('/admin/teams/')
def admin_teams():
    return 'Admin/Teams'


@app.route('/admin/teams/new')
def admin_teams_new():
    return 'Admin/Teams/New'


@app.route('/admin/teams/<name>/edit')
def admin_teams_edit():
    return 'Admin/Teams/Edit'
