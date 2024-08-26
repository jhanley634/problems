# Copyright 2024 John Hanley. MIT licensed.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world.<p>You're at the polls index.")
