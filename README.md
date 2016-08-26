# cuma

Installing
----------------------

### Installing dependencies

+ Python 2.7
+ pip
+ PostgreSQL >= 9.3
+ npm

#### Ubuntu 14.04 pre-setup

    sudo apt-get update
    sudo apt-get install postgresql postgresql-server-dev-9.3 git python-pip python-dev npm nodejs-legacy
    sudo pg_createcluster 9.3 main --start
    sudo npm install -g bower

#### PostgreSQL Configuration
    createdb -U postgres cuma
    or
    sudo -u postgres psql
    CREATE DATABASE cuma;

### Setting up a virtualenv
    Virtualenv is not required (but it's better to use it)
    sudo pip install virtualenv
    mkdir ~/.virtualenvs/
    virtualenv ~/.virtualenvs/cuma --no-site-packages

### Configure App
    source ~/.virtualenvs/cuma/bin/activate      # if you installed
    pip install -r requirements.txt
    cp localsettings.example.py localsettings.py

### Set up your django environment
    ./manage.py migrate
    bower install
    ./manage.py collectstatic
    ./manage.py runserver

### Code style
    source ~/.virtualenvs/cuma/bin/activate      # if you installed
    pip install flake8
    git diff origin/master | flake8 --diff # If output is empty then your changes are good to go
