# Generated by Django 4.2.4 on 2023-10-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icq_new', '0006_remove_chat_last_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]