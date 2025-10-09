from django.urls import path

from . import views

urlpatterns = [
    path("clients/", views.client_list, name="client_list"),
    path("clients/update/<int:client_id>/", views.client_update, name="client_update"),
    path("clients/query/<int:client_id>/", views.client_query, name="client_query"),
    path("companies/", views.company_list, name="company_list"),
    path("companies/create/", views.company_create, name="company_create"),
    path("companies/update/<int:company_id>/", views.company_update, name="company_update"),
    path("companies/query/<int:company_id>/", views.company_query, name="company_query"),
]
