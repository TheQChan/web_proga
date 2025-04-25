from django.contrib import admin
from .models import Movie, UserProfile, MovieRating, Comment


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "is_popular", "created_at")
    list_filter = ("is_popular", "release_date")
    search_fields = ("title", "description")
    list_editable = ("is_popular",)
    date_hierarchy = "release_date"
    fieldsets = (
        ("Основная информация", {"fields": ("title", "description", "release_date")}),
        ("Изображения", {"fields": ("poster", "hero_image")}),
        ("Настройки", {"fields": ("is_popular",)}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
    search_fields = ("user__username", "bio")


@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__user__username", "movie__title")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "movie__title", "text")
