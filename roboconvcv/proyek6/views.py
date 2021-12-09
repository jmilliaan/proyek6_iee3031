from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello world, youre at the proyek 6 index")
# Create your views here.
