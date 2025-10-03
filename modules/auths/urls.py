from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_app, name="login"),
    path("logout/", views.logout_app, name="logout"),
    path("users/", views.users_list, name="users_list")
]