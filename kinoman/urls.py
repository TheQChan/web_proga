from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from movies import views
from django.contrib.auth import views as auth_views
from movies.views import add_comment, get_comments


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('rate-movie/<int:movie_id>/', views.rate_movie, name='rate_movie'),
    path('add-comment/<int:movie_id>/', add_comment, name='add_comment'),
    path('comments/<int:movie_id>/', get_comments, name='get_comments'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
