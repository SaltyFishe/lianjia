from django.contrib import admin

# Register your models here.
from .models import House, MyUser

admin.site.register(House)
admin.site.register(MyUser)
