# Lego Challenge
## Requirements
- Python 3.4+
- Pip - Comes with Python 3.4+. Note that some older version no longer work so try and upgrade it to the most recent version if possible.
- SQLite 3 - Should be provided with Python, but having it installed specifically allows you to manually interact with the database which is useful for debugging.

Python3.3+ should provide access to the `venv` module for creating a virtual environment. However, some Linux distibutions tweaked the Python installation so you may need to install an additional
package. Check your distibution for more details. For windows installations, it may be easier to avoid using a virtual envronment and installing the required Python dependencies globally.

There have been reports that Python 3.6 has a problem that breaks the use of Sqlite. This hasn't been verified, but if you do see a problem in this area, it is suggested to use Python 3.4 instead.

## Browsers
The application has been tested on the latest version of the following browsers (as of Jan 2019):
- Chrome
- Firefox

Older browsers may have issues in the layout and styling of the application. If this does occur, please ensure your browser is up to date. Alternatively, try another tested browser. There is also a known issue with Microsoft Edge so it is highly recommended you avoid this browser.

## Setup
### Linux
A script has been provided to set up the required environment for Linux distributions:
```bash
$ git clone <repository>
$ cd ./<repository>
$ . ./setup.sh
```
Note that the first `.` before running `setup.sh` is required otherwise the virtual environment won't activate properly. If you miss it, run `source ./venv/bin/activate` afterwards.

The setup script will skip installing python dependencies if it thinks they are installed already. Note that this is a very basic check and may not be entirely correct. If the dependencies are not installed or are out of date, simply delete the `venv` directory and try again.

## Using the Appication
### Initialisation
Once you have installed the dependencies, copy `<path\to\repository>\lego\config.sample.py` to `<path\to\repository>\lego\config.py` and run the following:
```bash
# create database and default users
# you will be prompted for user passwords here
$ flask init
```

### Adding Teams
To add the teams for the day to the database, run:
```bash
$ flask add-teams <path/to/teams.txt>
```
An example teams.txt file can be found at `teams_example.txt`.

The file format is as follows with one number and name pair per line:
```txt
number, name
```

### Run the Application
To run the application, simply run:
```bash
$ flask run
```
This will run the application on port 5000 of localhost, e.g. `http://localhost:5000`.

There are a number of options to customise the running of the application further:
- `--host=<ip address>` - Alters the IP address the appication runs on. This is essential for usage outside of the standard localhost. The most common usage will be `--host=0.0.0.0` which connects the application to all network interfaces allowing it to be accessed from other computers. With this active, all another computer needs to connect is your IP address and the port the application is running on, e.g. `1.2.3.4:5000`.
- `--port=<port>` - Configures the port the application runs on. Useful for setting the port to `80` to allow the port to be left off the address as `80` is the standard port for HTTP.
- `--with-threads` / `--without-threads` - By default multithreading is not enabled so you will have to add this handle or use the `run.sh` script. It is vital that this is enabled on the event days to handle many users. 

More options can be found by using `flask run --help`. Alternatively a script to start the application with common options pre-set can be found at `run.sh`:

```
$ ./run.sh &
```

To halt the application, use `Ctrl+C`. If you are using the provided `run.sh` script, use `fg` and then `Ctrl+C`.

If you wish to run the application for a long period of time, e.g. for the competition, using `screen` or running the application as a background process by appending `&` to the command may be more useful. Note that `&` is used in the example invocation of `run.sh` above.

Additionally, disabling debug mode by running the following will reduce the verbosity of the output to stdout. This is initialised to 1 by the setup scripts.
```
export FLASK_DEBUG=0
```

## Todo
- [ ] Add tests ([[1](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing)] and 2nd from last part).
    - [ ] Add tests for cli
    - [ ] Add tests for team model
    - [ ] Add tests for util
- [ ] Add JavaScript form helpers for rounds that have bonus points, e.g. disable checkboxes unless pre-requisites have been met.
- [ ] Clean up and document code for maintainability.
- [ ] Improve teams cli:
    - `flask team add [--number NUMBER --name NAME | --file PATH_TO_FILE]`
    - `flask team list [--no-practice] [--active]`
    - `flask team reset [-y]`
- [ ] Assess common code between Bristol and UK finals:
    - `Make Bristol use UK html template`
