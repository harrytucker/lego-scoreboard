# Lego Challenge
## Requirements
- Python 3.4+
- Pip - Comes with Python 3.4+. Note that some older version no longer work so try and upgrade it to the most recent version if possible.
- SQLite 3 - Should be provided with Python, but having it installed specifically allows you to manually interact with the database which is useful for debugging.

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
Note that the first `.` before running `setup.sh` is required otherwise the virtual environment won't activate properly. If you miss it, run `source ./venv/bin/activate` afterwards.

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
# clone this repository using Git Bash or other Git tool
git clone <repository>

# using cmd.exe
cd <path\to\repository>

# experimental script for installing dependencies
setup

# or manually install dependencies
pip install -r requirements.txt
set FLASK_APP=<path\to\repository>\lego\__init__.py
set FLASK_DEBUG=1
```
It is probably possible to use a virtual envronment on Windows, but it hasn't been tested, so the dependencies are installed globally.

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
An example teams.txt file can be found at `teams_example.txt`.

The file format is as follows with one number and name pair per line:
```
number, name
```

### Run the Application
To run the application, simply run:
```
$ flask run
```
This will run the application on port 5000 of localhost, e.g. `http://localhost:5000`.

You can modify the command to run on all assigned IP addresses:
```
$ flask run --host=0.0.0.0
```
This usage is usually required to run and access the application on Windows.

You can also change the used port to `80` to avoid specifying it in the browser:
```
$ flask run --host=0.0.0.0 --port=80
```

To halt the application, use `Ctrl+C`.

If you wish to run the application for a long period of time, e.g. for the competition, using `screen` or running the application as a background process by appending `&` to the command may be more useful.

Additionally, disabling debug mode by running the following will reduce the verbosity of the output to stdout. This is initialised to 1 by the setup scripts.
```
# for linux
export FLASK_DEBUG=0

# for windows
set FLASK_DEBUG=0
```

## Todo
- [ ] Add logging where appropriate.
- [ ] Add unit testing ([[1](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing)] and 2nd from last part).
- [ ] Create proper manual (see questions in emails plus other relevant data/hacks that may be required).
- [ ] Add simulation mode for quickly filling out data to simulate the event.
- [X] Add CSS (In progress).
    - [X] Use columns for scoreboard rather than floats.
- [ ] Add JavaScript form helpers for rounds that have bonus points, e.g. disable checkboxes unless pre-requisites have been met.
- [X] Implement Bristol scoreboard.
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
- [X] Implement something for telling teams where to go for quarter/semi/finals.
- [ ] Add other tasks to complete here.
