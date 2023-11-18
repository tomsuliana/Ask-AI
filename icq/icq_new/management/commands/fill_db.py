from django.core.management.base import BaseCommand
from icq_new.models import *
from faker import Faker
import random


class Command(BaseCommand):
    help = "filling databse with random data"
    fake = Faker()

    def create_fake_users(self, count):
        print('users creation started')
        words = list(set(self.fake.words(nb=10000)))
        random.shuffle(words)
        usernames = []
        i = 0
        while i < count:
            for first_word in words:
                for second_word in words:
                    usernames.append(first_word + second_word)
                    i += 1
        users = [User(username=usernames[i],
                    email = self.fake.email(),
                    password = self.fake.password())
                for i in range(count)]

        User.objects.bulk_create(users)
        print('users done')

    def create_fake_chats(self, count):
        print('chats creation started')
        users = User.objects.all()
        chats = []
        for i in range (count):
            members_to_add = random.choices(users, k=2)
            chat = Chat(members=members_to_add)
            chats.append(chat)
        Chat.objects.bulk_create(chats)
        print('chats done')

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        users_count = ratio
        chats_count = ratio

        self.create_fake_users(users_count)
        self.create_fake_chats(chats_count)