# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import render_template

from . import app
from .forms import LoginForm
from .models import Team

@app.route('/')
@app.route('/home')
def home():
    teams = Team.query.all()
    return render_template('home.html', title='Home', teams=teams)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    return 'Logout'


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
