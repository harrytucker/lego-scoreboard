#! /usr/bin/env bash
# -------------------------------------------------------------------------------------------------
# Setup script for Lego Challenge site.
# -------------------------------------------------------------------------------------------------

if [[ ! -d "./venv" ]]; then
    echo "Creating new virtual environment..."
    python3 -m venv ./venv
else
    echo "Virtual environment already exists. Skipping..."
fi

echo "Activating virtual environment..."
source ./venv/bin/activate

if [[ ! $(pip show flask | grep "Name: Flask") ]]; then
    echo "Installing dependencies via pip..."
    pip install -r requirements.txt
else
    echo "Dependencies already installed. Skipping..."
fi

echo "Setting requirement environment variables..."
export FLASK_APP="`pwd`/lego/__init__.py"
export FLASK_DEBUG=1

echo "Done"
