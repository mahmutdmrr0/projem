from django.urls import path
from libraryapp import views


urlpatterns = [
    path("",views.index),
]