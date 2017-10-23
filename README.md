# Lego Challenge
## Setup
Requirements:
- Python 3.4+
- Pip (should be installed with Python3.4)
- SQLite 3 (not required, but can be helpful for debugging)

Python3.3+ should provide access to the venv module for creating a virtual environment. However, some Linux distibutions tweaked the Python installation so you may need to install an additional package. Check your distibution for more details.

Once your dependencies are installed:
```bash
$ cd /path/to/lego

# create virtual environment and activate it
$ python3 -m venv ./venv
$ source ./venv/vin/activate

# install dependencies
$ pip install -r ./requirements.txt

# set required environment variables
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

##
