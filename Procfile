release: sh -c 'python3 manage.py sqlflush | python3 manage.py dbshell && python3 manage.py makemigrations Grooving && python3 manage.py migrate'
web: sh -c 'gunicorn Server.wsgi --log-file - && python3 utils/whooshSearcher/indexing.py'
