set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
python3.8 manage.py collectstatic
python manage.py migrate
