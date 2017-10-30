# Lego Challenge
## Setup
Requirements:
- Python 3.4+
- Pip - Should be installed with Python3.4.
- SQLite 3 - Not required, but can be helpful for debugging database issues. Python3 supports it out the box.

Python3.3+ should provide access to the `venv` module for creating a virtual environment. However, some Linux distibutions tweaked the Python installation so you may need to install an additional package. Check your distibution for more details.

Once your dependencies are installed and this repository has been cloned:
```bash
$ cd /path/to/lego

# create virtual environment and activate it
$ python3 -m venv ./venv
$ source ./venv/vin/activate

# install dependencies
$ pip install -r ./requirements.txt

# set required environment variables
# for windows use `set` instead of `export`
$ export FLASK_APP=/path/to/logo/__init__.py
# optional, helpful for debugging
$ export FLASK_DEBUG=1

# create config file from sample
$ cp ./config_sample.py ./config.py

# generate secret key
# copy this value into SECRET_KEY in your config.py
$ flask generate-secret-key

# create database and default users
# you will be prompted for user passwords here
$ flask init
```

## Usage
To run the application, simply run:
```bash
$ flask run
```

For windows, you may need to use:
```bash
$ flask run --host=0.0.0.0
```

To halt the application, use `Ctrl+C`.

## Todo
- Implement checkpoints on tasks page.
- Uncomment refresh tag on scoreboard page.
- Log errors to a file see [[1](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing)].
- Add unit testing (above and 2nd from last part).
- Use flask-bcrypt.


## Maintaince and Updates
This application has been built with the idea that it will be passed on to future maintainers. For example, Flask was chosen because it is written in a commonly taught language and has a number of guides and help resources available.

The following resources were used to create the original application which may be of use for future updates or answer questions about how certain parts work:

- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

Flask also provides a number of quickstart guides for both the main Flask module and it's supported extensions. Many of the extensions wrap pre-existing modules. The following pages may also be of use when updating the code:

- [Flask](http://flask.pocoo.org/) ([Quickstart](http://flask.pocoo.org/docs/0.12/quickstart/))
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) ([Quickstart](http://flask-sqlalchemy.pocoo.org/2.3/quickstart/))
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) ([Quickstart](http://flask-wtf.readthedocs.io/en/stable/quickstart.html))
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [WTForms](https://wtforms.readthedocs.io/en/latest/)
- [Jinja2](http://jinja.pocoo.org/docs/2.9/)
- [Click](http://click.pocoo.org/5/)
