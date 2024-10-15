# Copyright 2024 John Hanley. MIT licensed.
from django.http import HttpResponse, Request
from django.shortcuts import render

assert render


def index(request: Request) -> HttpResponse:
    assert request
    return HttpResponse("Hello, world.<p>You're at the polls index.")
