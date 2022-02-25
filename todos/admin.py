from django.contrib import admin
from .models import User, Todo

# Register your models here.

admin.site.register([Todo, User])
