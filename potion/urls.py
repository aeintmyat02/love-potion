from django.urls import path
from . import views

urlpatterns = [
    path("", views.initial_page, name="initial_page"),
    path("mix/", views.mix_page, name="mix_page"),
    path("result/", views.result_page, name="result_page"),
    path("clear/", views.clear_session, name="clear_session"),
]