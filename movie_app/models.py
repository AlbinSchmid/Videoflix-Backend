from django.db import models
from django.utils.text import slugify

# Create your models here.


class Movie(models.Model):
    CATEGORY_CHOICES = [
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Animation', 'Animation'),
        ('Comedy', 'Comedy'),
        ('Crime', 'Crime'),
        ('Documentary', 'Documentary'),
        ('Drama', 'Drama'),
        ('Family', 'Family'),
        ('Fantasy', 'Fantasy'),
        ('History', 'History'),
        ('Horror', 'Horror'),
        ('Music', 'Music'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Science Fiction', 'Science Fiction'),
        ('Sport', 'Sport'),
        ('Thriller', 'Thriller'),
        ('War', 'War'),
        ('Western', 'Western'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='movies')
    movie_cover_phone = models.FileField(upload_to='phone_covers')
    movie_cover = models.FileField(upload_to='covers')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
