set -e

export NEW_RELIC_APP_NAME=serverthrallapi.celery

newrelic-admin run-program \
    celery worker \
    --app=serverthrallapi.celery_app \
    --beat \
    --scheduler django
