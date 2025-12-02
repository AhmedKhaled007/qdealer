FROM python:3.9-slim-buster

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./carmarket /app/carmarket
COPY ./alembic /app/alembic
COPY alembic.ini entrypoint.sh  /app/

WORKDIR /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
