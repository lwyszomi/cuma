#!/usr/bin/env bash

source ./env.sh

# Fetch latest changes
su - cuma -s /bin/bash -c "cd $CUMA_APP_PATH; git checkout master; git pull origin master"

# Install Python dependencies
su - cuma -s /bin/bash -c "$CUMA_VENV_PATH/bin/pip install -r $CUMA_APP_PATH/requirements.txt"

# Run DB migrations
su - cuma -s /bin/bash -c "$CUMA_VENV_PATH/bin/python $CUMA_APP_PATH/manage.py migrate"

# Install Bower depedencies
su - cuma -s /bin/bash -c "cd $CUMA_APP_PATH; bower install"

# Collect static files
su - cuma -s /bin/bash -c "$CUMA_VENV_PATH/bin/python $CUMA_APP_PATH/manage.py collectstatic --clear --noinput"

# uWSGI restart
systemctl restart uwsgi
