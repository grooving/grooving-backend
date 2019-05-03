from django.contrib import admin
from .models import SystemConfiguration
from django.contrib.auth.models import User, Group
from django.contrib import admin

admin.site.register(SystemConfiguration)
admin.site.unregister(User)
admin.site.unregister(Group)
