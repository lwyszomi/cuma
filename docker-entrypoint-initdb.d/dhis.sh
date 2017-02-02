#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER dhis WITH PASSWORD 'dhis';
    CREATE DATABASE dhis;
    GRANT ALL PRIVILEGES ON DATABASE dhis TO dhis;
EOSQL
