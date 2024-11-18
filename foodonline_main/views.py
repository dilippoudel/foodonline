from django.shortcuts import render
from django.http import HttpResponse # noqa 


def home(request):
    return render(request, 'home.html')
