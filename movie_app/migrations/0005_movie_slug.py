# Generated by Django 5.1.7 on 2025-04-12 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0004_movie_movie_cover_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
