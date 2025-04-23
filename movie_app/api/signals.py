from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from movie_app.models import Movie
from .tasks import convert_hls, compress_image
import os
import django_rq
import shutil

@receiver(post_save, sender=Movie)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        if instance.movie_cover:
            queue.enqueue(compress_image, instance.movie_cover.path)
        if instance.movie_cover_phone:    
            queue.enqueue(compress_image, instance.movie_cover_phone.path)
        qualities = [('360p', 360), ('480p', 480), ('720p', 720), ('1080p', 1080)]
        for quality_name, quality_height in qualities:
            queue.enqueue(convert_hls, instance.slug, instance.video_file.path, quality_name, quality_height)


@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    target_path = os.path.join("media", "movies", instance.slug)

    if instance.movie_cover:
        if os.path.exists(instance.movie_cover.path):
            os.remove(instance.movie_cover.path)
    if instance.movie_cover_phone:
        if os.path.exists(instance.movie_cover_phone.path):
            os.remove(instance.movie_cover_phone.path)
    if os.path.exists(target_path):
        shutil.rmtree(target_path) 
    
                       