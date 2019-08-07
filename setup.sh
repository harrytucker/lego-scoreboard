#! /usr/bin/env bash
# -------------------------------------------------------------------------------------------------
# Setup script for Lego Challenge site.
# -------------------------------------------------------------------------------------------------
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export FLASK_APP="`pwd`/lego/__init__.py"
export FLASK_DEBUG=1

if [[ ! -f "./lego/config.py" ]]; then
    echo "Creating config file"
    cp ./lego/config.sample.py ./lego/config.py

    echo "Generating secret key and adding to config"
    SECRET_KEY=$(flask secret)
    # use | instead of / as base64 chars include /
    sed -i "s|your-secret-key|$SECRET_KEY|" ./lego/config.py
fi

