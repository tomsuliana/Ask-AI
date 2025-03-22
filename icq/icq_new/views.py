from django.shortcuts import render, redirect
from icq_new.forms import  LoginForm, RegistrationForm, SettingsForm
from django.views.decorators.http import require_GET
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from icq_new.models import *
from django.urls import reverse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
import json
import os


# Create your views here.


def index(request):
    # chats_with_messages = []
    #
    # for chat in Chat.objects.by_person(username=username):
    #     pair = [chat, "massege object here"]
    #     chats_with_messages.append(pair)
    user = request.user
    context = {
        'chats': Chat.objects.by_person(username=user.username),
        'last_messages': MESSAGES,
        'name': "Ai"
    }
    return render(request, 'index.html', context=context)


def dialog(request, current_username, chat_id):
    context = {
        'chats': Chat.objects.by_person(username=current_username),
        'messages': Message.objects.by_chat(chat_id=chat_id),
        'chat_id': chat_id,
    }
    if request.method == "POST":
        sender = request.user
        chat = get_object_or_404(Chat, id=chat_id)
        # params = QueryDict(request.body)
        # print(request.body)
        # print(params.dict().keys())
        # Access the value associated with the key 'text'
        # text = params.dict().get('text')

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        text = body['text']

        message = Message(sender=sender, chat=chat, text=text)
        message.save()
    return render(request, 'dialog.html', context=context)


def send_message(self, request):
    sender = request.user
    chat = request.POST['chat']
    text = request.POST['text']

    message = Message(sender=sender, chat=chat, text=text)
    message.save()
    return render(request, 'dialog.html', context=context)

def log_in(request):
    # us = User.objects.filter(username="uliana")
    # print(us[0].password)
    if request.method == "GET":
        login_form = LoginForm()
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse(request.POST['continue_']))
                # return render(request, 'index.html')
            else:
                login_form.add_error(None, "Invalid username or password")
    return render(request, 'login.html', context={'form': login_form})

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def signup(request):
    if request.method == "GET":
        register_form = RegistrationForm()
    elif request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            us = new_user_(request.POST)
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = auth.authenticate(request=request, **login_form.cleaned_data)
                if user:
                    login(request, user)
                    return redirect(reverse('index'))

    return render(request, 'signup.html', context={'form': register_form})

@login_required
def settings(request):
    user = request.user

    if request.method == "POST":
        form = SettingsForm(request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = SettingsForm(instance=user)
    return render(request, 'settings.html', context={'form': form})


def start_dialog(request, member="None"):
    models = get_file_names('/media/uliana/Data/Article/models')
    context = {
        'persons': User.objects.all(),
        'models': models,
    }

    if request.method == "POST":
        member1 = request.user
        member2 = User.objects.get(username=member)
        chat = Chat()
        chat.save()
        chat.members.add(member1)
        chat.members.add(member2)
        chat.save()
        return redirect(reverse('index'))
    return render(request, 'start_dialog.html', context=context)


def get_file_names(directory):
    try:
        # Получаем список всех объектов в папке
        items = os.listdir(directory)
        # Фильтруем список, оставляя только файлы
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
        return files
    except FileNotFoundError:
        print(f"Ошибка: папка '{directory}' не найдена.")
        return []
    except PermissionError:
        print(f"Ошибка: доступ запрещен к папке '{directory}'.")
        return []



