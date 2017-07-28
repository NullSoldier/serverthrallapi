set -e

export NEW_RELIC_APP_NAME=serverthrallapi.app

chmod +x manage.py
./manage.py migrate

newrelic-admin run-program \
    gunicorn serverthrallapi.wsgi \
    --log-file -
