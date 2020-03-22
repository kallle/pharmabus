#!/bin/bash

sqlite3 db.sqlite < database/schema.sql
sqlite3 db.sqlite < database/population.sql
export FLASK_ENV=development
export FLASK_APP=main.py
exec flask run
