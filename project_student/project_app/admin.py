from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import User
# Register your models here.
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)
admin.site.register(User)



