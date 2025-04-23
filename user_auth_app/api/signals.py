from django.dispatch import receiver
from django.db.models.signals import post_save
from user_auth_app.models import CustomUser
from .emails import send_welcome_email
import django_rq

@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(send_welcome_email, instance)

