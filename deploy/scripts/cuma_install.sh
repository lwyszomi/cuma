#!/usr/bin/env bash

source ./env.sh

# Create the 'cuma' user
useradd --system --key MAIL_DIR=/dev/null --shell /sbin/nologin --no-create-home --home-dir /opt/cuma --comment "CUMA" cuma
install -v -o cuma -g cuma -m 0750 -d /opt/cuma

# git, gitignore for the 'cuma' user
yum -y install git
su - cuma -s /bin/bash -c "git config --global core.excludesfile ~/.gitignore_global"
su - cuma -s /bin/bash -c "curl -sL -o ~/.gitignore_global https://gist.githubusercontent.com/octocat/9257657/raw/3f9569e65df83a7b328b39a091f0ce9c6efc6429/.gitignore"

# SSH key for the 'cuma' user for GitHub deploys (add '/opt/cuma/.ssh/github_rsa.pub' contents to GitHub)
install -v -o cuma -g cuma -m 0700 -d /opt/cuma/.ssh
cp $CUMA_PRIVATE_KEY /opt/cuma/.ssh/github_rsa
chmod 400 /opt/cuma/.ssh/github_rsa
chown cuma /opt/cuma/.ssh/github_rsa
su - cuma -s /bin/bash -c "ssh-keyscan -t rsa github.com >> /opt/cuma/.ssh/known_hosts"

install -v -o cuma -g cuma -m 0600 -T /dev/null /opt/cuma/.ssh/config
install -v -o cuma -g cuma -m 0600 -T /dev/null /opt/cuma/.ssh/known_hosts
su - cuma -s /bin/bash -c "ssh-keyscan -t rsa github.com >> /opt/cuma/.ssh/known_hosts"

cat > /opt/cuma/.ssh/config <<'EOF'
Host github.com
    User git
    PreferredAuthentications publickey
    IdentityFile /opt/cuma/.ssh/github_rsa
EOF

install -o cuma -g cuma -m 0755 -d /opt/cuma/code
su - cuma -s /bin/bash -c "git clone -b master $CUMA_GITHUB_URL /opt/cuma/code"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to clone repo"
    exit 1
fi


# Allow Nginx to access the static files in /opt/cuma/code/static (parent dirs already have o=x)
if ( getent passwd nginx &>/dev/null ); then
  setfacl -m 'u:nginx:--x' /opt/cuma/
fi
# Allow uWSGI to access the code files in /opt/cuma/code (parent dirs already have o=x)
if ( getent passwd uwsgi &>/dev/null ); then
  setfacl -m 'u:uwsgi:--x' /opt/cuma/
fi

# Install the cuma venv to '/opt/cuma/venv'
install -o cuma -g cuma -m 0755 -d /opt/cuma/venv
su - cuma -s /bin/bash -c "virtualenv --no-site-packages /opt/cuma/venv"
#source /opt/cuma/venv/bin/activate
/opt/cuma/venv/bin/pip list | awk '{print $1}' | xargs --no-run-if-empty /opt/cuma/venv/bin/pip install --upgrade
/opt/cuma/venv/bin/pip install -r /opt/cuma/code/requirements.txt

# Extended the systemd unit for uWSGI to allow Nginx execute on the socket directory
if ( getent passwd nginx &>/dev/null ); then
  install -o root -g root -m 0755 -d /etc/systemd/system/uwsgi.service.d/
  cat > /etc/systemd/system/uwsgi.service.d/acl-nginx.conf <<EOF
[Service]
PermissionsStartOnly=true
ExecStartPre=/bin/setfacl -m 'u:nginx:--x' /run/uwsgi
EOF
fi
systemctl daemon-reload

# Copy uwsgi emperor settings for cuma app, make changes necessary for this system configuration
# - nginx needs 'rw' permissions on the socket (other users denied access via '/run/uwsgi/' permissions)
sed \
  -e 's%^\(socket[[:blank:]]*=[[:blank:]]*\).*%\1/run/uwsgi/cuma.sock%' \
  -e 's%/var/www/cuma%/opt/cuma/code%g' \
  -e 's%/opt/venv/cuma%/opt/cuma/venv%g' \
  -e 's%^#[[:blank:]]*\(chmod-socket\)%\1%' \
  -e '/^chmod-socket/ s/664/666/' \
  -e '$a\\n# Allow use of EPEL package uwsgi-plugin-python \nplugin = python' \
  /opt/cuma/code/deploy/cuma_uwsgi.ini \
  > /etc/uwsgi.d/cuma_uwsgi.ini
chmod -c --reference=/etc/uwsgi.ini /etc/uwsgi.d/cuma_uwsgi.ini
chown -c uwsgi:uwsgi /etc/uwsgi.d/cuma_uwsgi.ini

# PostgreSQL DB: username=cuma, password=cuma, database=cuma
createuser -U postgres --no-superuser --no-createdb --no-createrole cuma
psql -U postgres --command="ALTER USER cuma WITH PASSWORD 'cuma';"
createdb -U postgres -O cuma cuma
psql -U postgres --dbname=cuma --command="ALTER SCHEMA public OWNER TO cuma;"
cat >> /var/lib/pgsql/9.4/data/pg_ident.conf <<'EOF'
local_users    root               cuma
EOF
systemctl reload postgresql-9.4

# Set up localsettings.py for cuma, change database user and password, allow uwsgi user to read
sed \
  -e "s/\('USER':\) 'postgres'/\1 'cuma'/;" \
  -e "s/\('PASSWORD':\) 'password'/\1 'cuma'/;" \
  -e "/^SITE_ROOT/ a STATIC_URL = SITE_ROOT + '/static/'" \
  /opt/cuma/code/localsettings.production.py \
  > /opt/cuma/code/localsettings.py
chmod -c 00640 /opt/cuma/code/localsettings.py
chown -c cuma:uwsgi /opt/cuma/code/localsettings.py

# Initialize cuma app database, and download required files
cat << EOF | su - cuma -s '/bin/bash'
source /opt/cuma/venv/bin/activate
cd /opt/cuma/code/
python manage.py migrate
composer install
bower install
python manage.py collectstatic --noinput
EOF

# Create initial super-user for cuma
su - cuma -s '/bin/bash' -c "source /opt/cuma/venv/bin/activate && /opt/cuma/code/manage.py createsuperuser --username admin"

# Configure app
psql -U cuma cuma <<EOSQL
INSERT INTO accounts_cometserverconfiguration(url, username, password)
VALUES ('$DHIS2_URL',
        '$DHIS2_SUPERUSER_USERNAME_CUMA',
        '$DHIS2_SUPERUSER_PASSWORD_CUMA');
EOSQL

# Start uwsgi and cuma application
systemctl start uwsgi
systemctl restart uwsgi

# Add /cuma to Nginx
# - nginx needs 'x' permissions on '/run/uwsgi/' and subdirs, and 'rw' on '/run/uwsgi/cuma.sock' (configure above)
# - nginx needs 'x' permissions on '/opt/cuma/code' and subdirs, and 'r-x' on '/opt/cuma/code/static' (configure above)
NGINX_TMPFILE="$(mktemp)"
cat > "$NGINX_TMPFILE" <<'EOF'

  # cuma
  location /cuma {
    charset  utf-8;

    client_max_body_size  75M;

    location /cuma/static {
      alias /opt/cuma/code/static;
      if ($uri ~* ".*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|swf|ico)" ) {
       expires max;
      }
    }

    uwsgi_pass          unix:///run/uwsgi/cuma.sock;
    include             uwsgi_params;
    uwsgi_read_timeout  600;
    uwsgi_param         REQUEST_SCHEME $scheme;
    uwsgi_param         SCRIPT_NAME /cuma;
    uwsgi_modifier1     30;
  }
EOF
sed -e "/server_name[[:blank:]]\+.*;/r $NGINX_TMPFILE" -i /etc/nginx/sites-available/default_server.conf
\rm "$NGINX_TMPFILE"
unset NGINX_TMPFILE
nginx -t && systemctl restart nginx

# Install the CUMA app
CUMA_TMPDIR="$( su - tomcat -s /bin/bash -c 'mktemp -d' )"
cp -a /opt/cuma/code/cuma-prod.zip "$CUMA_TMPDIR/cuma.zip"
install -o tomcat -g tomcat -d /opt/dhis2/apps/cuma/
yum -y install unzip
su - tomcat -s /bin/bash -c "unzip -d /opt/dhis2/apps/cuma/ $CUMA_TMPDIR/cuma.zip"
\rm -r "$CUMA_TMPDIR"
unset CUMA_TMPDIR

##

exit 0
