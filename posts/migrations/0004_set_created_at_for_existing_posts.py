from django.db import migrations
from django.utils import timezone

def set_created_at(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    for post in Post.objects.filter(created_at__isnull=True):
        post.created_at = timezone.now()
        post.save()

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0003_comment_author_alter_post_description_and_more'),
    ]

    operations = [
        migrations.RunPython(set_created_at),
    ] 