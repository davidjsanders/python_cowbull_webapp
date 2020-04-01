#!/bin/sh
if [ "$PORT" == "" ]
then
    PORT=8080
fi
gunicorn -b 0.0.0.0:$PORT -w 4 app:app
