# Generated by Django 5.1.5 on 2025-02-20 11:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_is_following', to=settings.AUTH_USER_MODEL)),
                ('user_follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_is_followed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
