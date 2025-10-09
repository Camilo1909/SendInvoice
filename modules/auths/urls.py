from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_app, name="login"),
    path("logout/", views.logout_app, name="logout"),
    path("users/", views.users_list, name="users_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/assign_password/", views.assign_password, name="user_assign_password"),
    path("users/update/<int:user_id>/", views.user_update, name="user_update"),
    path("users/query/<int:user_id>/", views.user_query, name="user_query"),
]
