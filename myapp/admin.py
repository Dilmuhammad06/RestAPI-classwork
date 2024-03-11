from django.contrib import admin
from .models import User,UserCodeVerify

admin.site.register([User,UserCodeVerify])