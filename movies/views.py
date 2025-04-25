from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Movie, UserProfile, MovieRating, Comment
from .forms import RegistrationForm
from django.utils import timezone


def index(request):
    featured_movie = Movie.objects.filter(is_popular=True).last()
    popular_movies = Movie.objects.filter(is_popular=True).order_by("-created_at")[:10]

    return render(
        request,
        "movies/index.html",
        {"featured_movie": featured_movie, "popular_movies": popular_movies},
    )


def about(request):
    return render(request, "movies/about.html")


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = Comment.objects.filter(movie=movie).order_by("-created_at")
    user_rating = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            rating = MovieRating.objects.filter(user=user_profile, movie=movie).first()
            if rating:
                user_rating = rating.rating
        except UserProfile.DoesNotExist:
            pass

    return render(
        request,
        "movies/movie_detail.html",
        {"movie": movie, "comments": comments, "user_rating": user_rating},
    )


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_ratings = MovieRating.objects.filter(user=user_profile).select_related("movie")

    return render(
        request,
        "movies/profile.html",
        {"user_profile": user_profile, "user_ratings": user_ratings},
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        if "avatar" in request.FILES:
            user_profile.avatar = request.FILES["avatar"]
        user_profile.bio = request.POST.get("bio", "")
        user_profile.save()
        messages.success(request, "Профиль успешно обновлен")
        return redirect("profile")
    return redirect("profile")


@login_required
def rate_movie(request, movie_id):
    if request.method == "POST":
        rating_value = request.POST.get("rating")
        if rating_value:
            movie = get_object_or_404(Movie, id=movie_id)
            user_profile = UserProfile.objects.get(user=request.user)
            rating, created = MovieRating.objects.get_or_create(
                user=user_profile, movie=movie, defaults={"rating": rating_value}
            )
            if not created:
                rating.rating = str(6 - int(rating_value))
                rating.save()
            messages.success(request, "Оценка сохранена")
    return redirect("movie_detail", movie_id=movie_id)


@login_required
def add_comment(request, movie_id):
    if request.method == "POST":
        comment_text = request.POST.get("comment", "").strip()
        if not comment_text:
            return JsonResponse(
                {"success": False, "error": "Комментарий не может быть пустым"},
                status=400,
            )

        movie = get_object_or_404(Movie, id=movie_id)
        comment = Comment.objects.create(
            user=request.user, movie=movie, text=comment_text
        )

        return JsonResponse(
            {
                "success": True,
                "comment": {
                    "user": request.user.username,
                    "text": comment.text,
                    "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M"),
                },
                "last_update": timezone.now().isoformat(),
            }
        )
    return JsonResponse({"success": False}, status=400)


def get_comments(request, movie_id):
    since = request.GET.get("since")
    movie = get_object_or_404(Movie, id=movie_id)

    comments_query = movie.comment_set.all().order_by("-created_at")

    if since:
        try:
            since_date = timezone.datetime.fromisoformat(since)
            comments_query = comments_query.filter(created_at__gt=since_date)
        except (ValueError, TypeError):
            pass

    comments = list(comments_query.values("user__username", "text", "created_at")[:50])

    # Форматируем дату для каждого комментария
    for comment in comments:
        comment["created_at"] = timezone.datetime.strftime(
            comment["created_at"], "%d.%m.%Y %H:%M"
        )
        comment["user"] = comment["user__username"]

    return JsonResponse(
        {"comments": comments, "last_update": timezone.now().isoformat()}
    )


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, "Регистрация успешна. Теперь вы можете войти.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})
