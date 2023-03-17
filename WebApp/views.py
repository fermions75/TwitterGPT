from django.contrib.sites import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    # return HttpResponse("<h1> TwitterGPT Starts Here! </h1>")
    return render(request, 'index.html')