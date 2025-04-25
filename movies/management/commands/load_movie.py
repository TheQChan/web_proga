import requests
from django.core.management.base import BaseCommand

from movies.models import Movie

URL_POPULAR_MOVIE = "https://api.themoviedb.org/3/movie/popular?language=ru-RU&page=1"
HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NmU0YmFlYTJmZTAyOTIxZGQwNTIwNTc5OGFkMTcxNCIsIm5iZiI6MTczOTM2MjkwMi44NDYwMDAyLCJzdWIiOiI2N2FjOTI1NjIxZDBhOTJkNGI5YmFhODEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.5Z4kyrG5xW450AGbG2oJoFceK0464bk4FyZGuqjHAUQ",  # Замените на ваш токен
}
URL_IMG = "https://image.tmdb.org/t/p/original"


class Command(BaseCommand):
    help = "Загрузка популярных фильмов по API"

    def handle(self, *args, **kwargs):

        try:
            response = requests.get(URL_POPULAR_MOVIE, headers=HEADERS)
            data = response.json()
            for movie_data in data["results"]:
                if not Movie.objects.filter(title=movie_data["title"]).exists():
                    movie = Movie(
                        title=movie_data["title"],
                        description=movie_data["overview"],
                        release_date=movie_data["release_date"],
                    )
                    movie.save()
                    poster_url = URL_IMG + movie_data["poster_path"]
                    movie.download_poster(poster_url)
                    hero_url = URL_IMG + movie_data["backdrop_path"]
                    movie.download_hero_image(hero_url)
                    self.stdout.write(
                        self.style.SUCCESS(f"Добавлен фильм: {movie.title}")
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при запросе к API: {e}")
            )
