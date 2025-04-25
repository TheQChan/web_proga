from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from urllib.request import urlopen
import os


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    poster = models.ImageField(upload_to="posters/", verbose_name="Постер")
    hero_image = models.ImageField(
        upload_to="hero_images/",
        verbose_name="Картинка для главного экрана",
        null=True,
        blank=True,
    )
    release_date = models.DateField(verbose_name="Дата выхода")
    is_popular = models.BooleanField(default=True, verbose_name="Популярный")
    created_at = models.DateTimeField(auto_now_add=True)

    def download_poster(self, poster_url):
        """Метод для загрузки постера по URL."""
        result = urlopen(poster_url)
        self.poster.save(
            os.path.basename(poster_url),
            File(result),
            save=True
        )

    def download_hero_image(self, hero_url):
        """Метод для загрузки банера по URL."""
        result = urlopen(hero_url)
        self.hero_image.save(
            os.path.basename(hero_url),
            File(result),
            save=True
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    rated_movies = models.ManyToManyField(Movie, through="MovieRating")

    def __str__(self):
        return self.user.username


class MovieRating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
