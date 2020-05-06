#!/bin/bash

sqlite3 db.sqlite < data/schema.sql
sqlite3 db.sqlite < data/population.sql
export FLASK_ENV=development
export FLASK_APP=main.py
#python3 main.py
exec flask run
