from django.db import migrations, models
from django.utils.crypto import get_random_string, salted_hmac
from django.utils.encoding import force_bytes

def hash_email(email):
    """Hash an email address using HMAC with a random salt"""
    if not email:
        return ''
    salt = get_random_string(12)
    return salted_hmac(salt, force_bytes(email)).hexdigest()

def hash_existing_emails(apps, schema_editor):
    Comment = apps.get_model('posts', 'Comment')
    for comment in Comment.objects.all():
        if comment.author_email:
            comment.author_email_hash = hash_email(comment.author_email)
            comment.save()

def reverse_hash_emails(apps, schema_editor):
    # This is a no-op since we can't reverse the hashing
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0004_post_author_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author_email_hash',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.RunPython(
            hash_existing_emails,
            reverse_hash_emails
        ),
    ] 