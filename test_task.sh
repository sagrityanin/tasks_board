#! /bin/bash
if [ ! -f ./tests/venv/bin/activate ]; then
  echo "Create enviroment"
  python3 -m venv ./tests/venv
  cd tests
  source ./venv/bin/activate
  pip install -r requirements.txt
else
  echo "Environment exists"
  cd tests
  source ./venv/bin/activate
fi
#python3 make_tasks.py
python3 test_pagination.py
#python3 change_status_tasks.py
