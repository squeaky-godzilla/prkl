#!/bin/bash
cp ../../source/app.py .
cp -r ../../source/snippets .
docker-compose up --build &
