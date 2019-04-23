release: sh -c 'python3 manage.py sqlflush | python3 manage.py dbshell && python3 manage.py makemigrations Grooving && python3 manage.py migrate && python3 populate.py'

web: gunicorn Server.asgi:application -b 0.0.0.0:$PORT -k uvicorn.workers.UvicornWorker


