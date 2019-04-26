#!/usr/bin/env bash
python manager.py dbinit
gunicorn -c gunicorn.py manager:app --log-level debug
