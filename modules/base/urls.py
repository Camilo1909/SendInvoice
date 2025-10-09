from django.urls import path

from . import views

urlpatterns = [
    path("clients/", views.client_list, name="client_list"),
    path("clients/update/<int:client_id>/", views.client_update, name="client_update"),
    path("clients/query/<int:client_id>/", views.client_query, name="client_query"),
    path("companies/", views.company_list, name="company_list"),
]
