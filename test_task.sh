#! /bin/bash
python3 -m venv ./tests/venv
cd tests
source ./venv/bin/activate
pip install -r requirements.txt
python3 make_tasks.py
python3 test_pagination.py
python3 change_status_tasks.py
