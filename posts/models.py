from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string, salted_hmac
from django.utils.encoding import force_bytes

def hash_email(email):
    """Hash an email address using HMAC with a random salt"""
    if not email:
        return ''
    salt = get_random_string(12)
    return salted_hmac(salt, force_bytes(email)).hexdigest()

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    author_name = models.CharField(max_length=100)
    author_email_hash = models.CharField(max_length=128)  # Make hash field required
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def save(self, *args, **kwargs):
        if not self.author_email_hash:
            if self.author:
                self.author_email_hash = hash_email(self.author.email)
            else:
                raise ValueError("Email hash is required for comments")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"