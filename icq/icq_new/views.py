from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from icq_new.models import *

# Create your views here.
@require_GET
def index(request):
    context = {
        'messages': MESSAGES,
        'name': "Ai"
    }
    return render(request, 'index.html', context=context)


def dialog(request, name):
    context = {
        'messages': MESSAGES,
        'name': name,
    }
    return render(request, 'index.html', context=context)


def log_in(request):
    return render(request, 'login.html')


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')



