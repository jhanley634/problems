# Copyright 2024 John Hanley. MIT licensed.
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
