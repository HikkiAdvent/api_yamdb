from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser

admin.site.register(MyUser, UserAdmin)
