#!/bin/bash

alembic revision --autogenerate -m 'initial'
alembic upgrade head
python bot.py