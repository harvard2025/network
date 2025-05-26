
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newPost', views.newPost, name='newPost'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('UnFollow', views.unfollow, name='unfollow'),
    path('Follow', views.follow, name='follow'),
    path('following', views.Following, name='following'),
    path('edit/<int:post_id>', views.edit, name='edit'),
    path('remove_like/<int:post_id>', views.remove_Like, name='remove_like'),
    path('add_Like/<int:post_id>', views.add_Like, name='add_Like'),




    
]
