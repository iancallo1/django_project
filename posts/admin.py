from django.contrib import admin

# posts/admin.py
from .models import Post

admin.site.register(Post)
