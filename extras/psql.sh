#!/usr/bin/env bash
PGPASSWORD=$POSTGRES_PASSWORD psql --username $POSTGRES_USER --host $POSTGRES_HOST $POSTGRES_DB
