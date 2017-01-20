#!/bin/bash

# DHIS2 instance url address
DHIS2_URL=<SET_THIS_UP>

# DHIS2 superuser credentials, used to communicate with
DHIS2_SUPERUSER_USERNAME_CUMA=admin
DHIS2_SUPERUSER_PASSWORD_CUMA=district
DHIS2_SUPERUSER_USERNAME_SSC=admin
DHIS2_SUPERUSER_PASSWORD_SSC=district

# Reader Github & key URLS
READER_GITHUB_URL=git@github.com:theirc/dhis2.git
READER_PRIVATE_KEY=~/github_rsa

# CUMA Github & key URLS
CUMA_GITHUB_URL=git@github.com:theirc/CUMA.git
CUMA_PRIVATE_KEY=~/github_rsa

# Reader paths to code and virtualenv for update_reader.sh script
READER_APP_PATH=/opt/reader/code
READER_VENV_PATH=/opt/reader/venv

# CUMA paths to code and virtualenv for update_reader.sh script
CUMA_APP_PATH=/opt/reader/code
CUMA_VENV_PATH=/opt/reader/venv
