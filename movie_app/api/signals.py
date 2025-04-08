from django.dispatch import receiver
from .tasks import convert_480p
from django.db.models.signals import post_delete, post_save
from movie_app.models import Movie
import os
import django_rq

@receiver(post_save, sender=Movie)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_480p, instance.video_file.path)


@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.movie_cover:
        if os.path.exists(instance.movie_cover.path):
            os.remove(instance.movie_cover.path)
    if instance.movie_cover_phone:
        if os.path.exists(instance.movie_cover_phone.path):
            os.remove(instance.movie_cover_phone.path)
    if instance.video_file:
        if os.path.exists(instance.video_file.path):
            os.remove(instance.video_file.path)