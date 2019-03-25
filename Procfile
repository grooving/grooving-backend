release: sh -c 'python3 manage.py makemigrations && python3 manage.py migrate'
web: sh -c 'gunicorn Server.wsgi --log-file -' 
