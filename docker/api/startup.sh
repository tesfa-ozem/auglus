#!/bin/bash
dockerize -wait tcp://db:5432 -timeout 20s
pipenv run alembic upgrade head &&  pipenv run gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker app.server:app
