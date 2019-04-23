import os
import django

from channels.routing import get_default_application

# uvicorn Server.asgi:application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')
django.setup()
application = get_default_application()
