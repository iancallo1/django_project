from django.db import models

# posts/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title