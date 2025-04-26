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
        if comment.author:
            comment.author_email_hash = hash_email(comment.author.email)
        else:
            # For comments without an author, use a default hash
            comment.author_email_hash = hash_email('anonymous@example.com')
        comment.save()

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0006_merge_0004_and_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author_email',
        ),
        # First, make the field nullable with a default
        migrations.AlterField(
            model_name='comment',
            name='author_email_hash',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        # Then run the data migration to set values for all comments
        migrations.RunPython(
            hash_existing_emails,
            migrations.RunPython.noop
        ),
        # Finally, make the field required
        migrations.AlterField(
            model_name='comment',
            name='author_email_hash',
            field=models.CharField(max_length=128),
        ),
    ] 