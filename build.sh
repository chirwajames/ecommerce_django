set -o errexit
pip install -r requirements.txt
python3.9 manage.py collectstatic
python manage.py migrate