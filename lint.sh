#!/bin/bash
isort -rc main.py constants.py ex_client.py
autoflake -r --in-place --remove-unused-variables main.py constants.py ex_client.py
black -l 120 main.py constants.py ex_client.py
flake8 --max-line-length 120 main.py constants.py ex_client.py