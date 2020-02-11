#! /usr/bin/env bash
# -------------------------------------------------------------------------------------------------
# Setup script for Lego Challenge site.
# -------------------------------------------------------------------------------------------------
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export FLASK_APP="`pwd`/lego/__init__.py"
export FLASK_DEBUG=1

pip install -r requirements.txt

if [[ ! -f "./lego/config.py" ]]; then
    echo "Creating config file"
    cp ./lego/config.sample.py ./lego/config.py

    echo "Generating secret key and adding to config"
    SECRET_KEY=$(flask secret)
    # use | instead of / as base64 chars include /
    sed -i "s|your-secret-key|$SECRET_KEY|" ./lego/config.py
fi

# Create the database file if it does not exist, else the application will panic
if [[ ! -f "./lego/tmp/app.db" ]]; then
    echo "Creating application database..."
    flask init 
fi

# Create stage file if it is missing
if [[ ! -f "./lego/tmp/.stage" ]]; then
    echo "Creating stage file..."
    echo 0 > ./lego/tmp/.stage
fi

# Add teams
flask add-teams ./teams.txt
