#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:8001 manage:app
