#! /usr/bin/env bash
# -----------------------------------------------------------------------------
# Run flask application on any public IP address, on port 5000
# -----------------------------------------------------------------------------
export FLASK_APP="`pwd`/lego/__init__.py"
flask run --host=0.0.0.0 --port=5000 --no-debugger --with-threads --no-reload
