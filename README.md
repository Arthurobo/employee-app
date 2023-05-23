Run the following commands

pip install -r requirements.txt


python manage.py migrate

python manage.py createsuperuser
python manage.py runserver


Run this command to initiate elasticsearch
python manage.py search_index --rebuild


NOTE: You need elasticsearch installed and a postgres database to run this application successfully.