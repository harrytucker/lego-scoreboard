# Lego Challenge
## Requirements
- Python 3.4+
- Pip - Comes with Python 3.4+. Note that some older version no longer work so try and upgrade it to the most recent version if possible.

Python3.3+ should provide access to the `venv` module for creating a virtual environment. However, some Linux distibutions tweaked the Python installation so you may need to install an additional
package. Check your distibution for more details. For windows installations, it may be easier to avoid using a virtual envronment and installing the required Python dependencies globally.

## Setup
### Linux
A script has been provided to set up the required environment for Linux distributions:
```
$ git clone <repository>
$ cd ./<repository>
$ . ./setup.sh
```

Next you will need to initialise the application:
```
$ cd ./lego

# create config file from sample
$ cp ./config_sample.py ./config.py

# generate secret key
# copy this value into SECRET_KEY in your config.py
$ flask generate-secret-key

# create database and default users
# you will be prompted for user passwords here
$ flask init
```

### Windows
For Windows users, run the following:
```
# Clone this repository using Git Bash or other Git tool
git clone <repository>

# Using cmd.exe
cd <path\to\repository>

# Experimental script for installing dependencies
setup

# Or manually install dependencies
pip install -r requirements.txt
set FLASK_APP=<path\to\repository>\lego\__init__.py
set FLASK_DEBUG=1
```

Once you have installed the dependencies, copy `<path\to\repository>\lego\config.sample.py` to `<path\to\repository>\lego\config.py` and run the following:
```
# generate a secret key
# copy this value into SECRET_KEY in your config.py
flask generate-secret-key

# create database and default users
# you will be prompted for user passwords here
flask init
```

## Using the Appication
### Initialisation
Once you have installed the dependencies, copy `<path\to\repository>\lego\config.sample.py` to `<path\to\repository>\lego\config.py` and run the following:
```
# generate a secret key
# copy this value into SECRET_KEY in your config.py
flask generate-secret-key

# create database and default users
# you will be prompted for user passwords here
flask init
```

### Adding Teams
To add the teams for the day to the database, run:
```
$ flask add-teams <path/to/teams.txt>
```
An example teams.txt file can be found at `teams_example.txt`. There should be one team per line.

### Run the Application
To run the application, simply run:
```
$ flask run
```

For windows, you may need to use:
```
$ flask run --host=0.0.0.0
```

To halt the application, use `Ctrl+C`.

## Todo
- [ ] Uncomment refresh tag on scoreboard page.
- [X] Log errors to a file.
- [ ] Add logging where appropriate.
- [ ] Add unit testing ([[1](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing)] and 2nd from last part).
- [ ] Use flask-bcrypt for password encryption.
- [ ] Move maintenance and updates into separate file from README.
- [X] Add error handling to all forms
    - [X] Print out errors at top of form
    - [X] Add error class to relevant field
    - [X] Add styling to fields with errors
- [ ] Implement yellow cards.
- [ ] Implement red cards.
- [X] Save team points to the database.
    - [X] Handle multiple attempts (up to 3).
- [ ] Add CSS (In progress).
    - [X] Pad/Highlight nav icon only rather than entire nav list.
    - [ ] Use columns for scoreboard rather than floats.
    - [X] Center fields on login form.
- [ ] Add JavaScript form helpers for rounds that have bonus points, e.g. disable checkboxes unless pre-requisites have been met.
- [ ] Admin pages.
    - [X] Add routes
    - [ ] Correct team name.
    - [ ] Correct team number.
    - [ ] Adjust score.
    - [ ] Remove score.
- [ ] Finish implementing stages.
    - [ ] Persist current stage to a file.
    - [ ] Load stage from file on app start-up.
    - [ ] Add mechanism for increasing the stage through the UI (while the app is running).
- [ ] Dump db to file when moving stages to ensure nothing is lost.
    - [How to create and restore a backup from SqlAlchemy?](https://stackoverflow.com/questions/2786664/how-to-create-and-restore-a-backup-from-sqlalchemy)
- [ ] Implement Bristol scoreboard.
    - First round: 24 teams (3 tables of 8) with 3 attempts each.
    - Quarter final: 6 teams. Top vs. bottom, next top vs. next bottom, two middle teams:
        - Team 1 -> Table A
        - Team 2 -> Table C
        - Team 3 -> Table E
        - Team 4 -> Table F
        - Team 5 -> Table D
        - Team 6 -> Table B
    - Semi final: 4 teams.
        - Team 1 -> Table A
        - Team 2 -> Table C
        - Team 3 -> Table D
        - Team 4 -> Table B
    - Final: 2 teams (2 rounds).
        - Team 1 -> Table A
        - Team 2 -> Table B
        - (Then swap for 2nd round).
- [ ] Implement UK final scoreboard.
    - Current top 10 teams at top.
    - Cycle through remaining teams in batches of 10.
    - Keep current state for each refresh using a cache: [Caching](http://flask.pocoo.org/docs/0.12/patterns/caching/).
    - Top 8 teams progress, then 4, then 2 (knock out).
        - Team 1 -> Table A
        - Team 2 -> Table C
        - Team 3 -> Table E
        - Team 4 -> Table G
        - Team 5 -> Table H
        - Team 6 -> Table F
        - Team 7 -> Table D
        - Team 8 -> Table B
        - (And so on...)
- [ ] Add other tasks to complete here.

