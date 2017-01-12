# cuma

Initial setup (Docker)
-------------
* Linux
   * Install [Docker](https://docs.docker.com/engine/installation/)
   * Install [Docker Compose](https://docs.docker.com/compose/install/) (Note you can also install in a virtualenv with `$ pip install docker-compose`)

### Configuring App
    docker-compose build
    docker-compose run web python manage.py migrate

### Run application
    docker-compose up -d

### Configure CUMA
    Go to http://localhost:8080/ (It may take a while to load page for the first time). Sign in using login: admin, password: district
    Go to http://localhost:8080/dhis-web-maintenance-user/showAddUserForm.action
    Create new superuser in dhis2.
    docker-compose run web python manage.py create_or_update_config http://dhis:8080/ username password (Use username and password from user that you've created in previous step)

### Load fixtures (optional)
    Go to http://localhost:8080/dhis-web-importexport/dxf2MetaDataImport.action
    Choose dhis2-docker/fixtures/metadata.xml, change format to xml and then hit import button
    Repeat same process for dhis2-docker/fixtures/userRoleMetadata.xml (Order is important here)
    

Installing (Without Docker)
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
