from django.db import models
from django.utils.text import slugify
from user_auth_app.models import CustomUser

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
    release_year = models.IntegerField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='movies')
    movie_cover_phone = models.FileField(upload_to='phone_covers')
    movie_cover = models.FileField(upload_to='covers')
    author = models.CharField(max_length=255, default='', blank=True)
    author_url = models.CharField(max_length=255, default='', blank=True)
    license = models.CharField(max_length=255, default='', blank=True)
    license_url = models.CharField(max_length=255, default='', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class UserMovieProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    progress_seconds = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta: 
        unique_together = ('user', 'movie')
