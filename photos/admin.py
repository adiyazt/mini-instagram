from django.contrib import admin
from .models import User, Photo, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Photo)
admin.site.register(Comment)