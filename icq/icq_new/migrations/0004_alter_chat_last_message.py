# Generated by Django 4.2.4 on 2023-09-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icq_new', '0003_alter_chat_last_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='last_message',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
