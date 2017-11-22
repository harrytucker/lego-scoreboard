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
- [ ] Log errors to a file see [[1](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing)].
- [ ] Add logging where appropriate.
- [ ] Add unit testing (above and 2nd from last part).
- [ ] Use flask-bcrypt for password encryption.
- [ ] Move maintenance and updates into separate file from README.
- [ ] Add error handling to all forms
    - [X] Print out errors at top of form
    - [X] Add error class to relevant field
    - [ ] Add styling to fields with errors
- [ ] Implement yellow cards.
- [ ] Implement red cards.
- [X] Save team points to the database
    - [X] Handle multiple attempts (up to 3)
- [ ] Add CSS (In progress)
- [ ] Add JavaScript form helpers for rounds that have bonus points, e.g. disable checkboxes unless pre-requisites have been met.
- [ ] Add other tasks to complete here.

