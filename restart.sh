#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Restart script for the Lego Challenge site.
# Use this script to completely reset the state of the competition
# ------------------------------------------------------------------------------

# To reset the competition state we need to delete the app.db database and reset
# the stage file.
#
# Basically we nuke all the contents and go back to zero
if [[ -f "./lego/tmp/app.db" ]]; then
    echo "Deleting database..."
    rm ./lego/tmp/app.db
else
    echo "Database has already been deleted, please run setup.sh"
fi

echo "Resetting stage file..."
echo 0 > ./lego/tmp/.stage

echo "Restart done, please run the following next to begin:"
echo "    1. setup.sh to setup the database and config"
echo "    2. run.sh to run the application"
