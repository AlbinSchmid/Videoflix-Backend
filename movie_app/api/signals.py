from django.dispatch import receiver
from django.db.models.signals import post_delete
from movie_app.models import Movie
import os

@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.exists(instance.video_file.path):
            os.remove(instance.video_file.path)