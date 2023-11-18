from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

MESSAGES = [
    {
        'id': i,
        'sender': f'Awesome {i}',
        'text': f'Text {i} blablabla',
    } for i in range(12)
]

PERSONS = [
    {
        'id': i,
        'name': f'Person {i}',
    } for i in range(20)
]


class MessageManager(models.Manager):
    def by_chat(self, chat_id):
        queryset = self.get_queryset()
        return queryset.filter(chat=chat_id).order_by("timestamp")


class ChatManager(models.Manager):
    def by_person(self, username):
        queryset = self.get_queryset()
        return queryset.filter(members__username__exact=username).order_by("last_message")

    def __str__(self):
        return f"{self.name}"


    def name_by_user(self):
        return f"{self.members.all()}"


class UserManager(models.Manager):
    def by_chat(self, chat_id):
        queryset = self.get_queryset()
        return queryset.filter





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='static/avatars/', default='static/img/img.png')


class Chat(models.Model):
    members = models.ManyToManyField(User)
    last_message = models.DateTimeField(default=None, blank=True, null=True)

    objects = ChatManager()

    @property
    def title(self):
        return self.members.all()

    @property
    def last_message_text(self):
        return self.messages.all().last()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return f"{self.text}"


def new_user_(us):
    new_user = User.objects.create_user(username=us['username'], first_name=us['first_name'], last_name=us['last_name'],
                                      email=us['email'], password=us['password'])
    profile = Profile(user=new_user)
    profile.save()
    return new_user

def new_message_(mes):
    new_message = Message.objects.create_message(sender=mes['sender'], chat=mes['chat'], text=mes['text'])
    return new_message



