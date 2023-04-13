#!/bin/sh

#Run database migration
echo "Running database migration"
alembic upgrade head
# Run the software squire
uvicorn qdealer.app:app --host 0.0.0.0 --port 8000 --reload
#