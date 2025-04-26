from django.contrib import admin

# posts/admin.py
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)