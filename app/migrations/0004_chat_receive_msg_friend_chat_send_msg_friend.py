# Generated by Django 4.2.6 on 2023-11-07 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_addfriends_receive_friends_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='receive_msg_friend',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='send_msg_friend',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]