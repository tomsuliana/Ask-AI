from django.db import models

# Create your models here.

MESSAGES = [
    {
        'id': i,
        'sender': f'Awesome {i}',
        'text': f'Text {i} blablabla',
    } for i in range(12)
]