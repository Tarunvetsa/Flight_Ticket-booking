from django.contrib import admin
from .models import Flight, User

admin.site.register(User)
admin.site.register(Flight)