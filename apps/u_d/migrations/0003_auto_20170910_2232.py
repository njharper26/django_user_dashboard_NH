# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-11 03:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('u_d', '0002_auto_20170910_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_desc', to='u_d.User')),
            ],
        ),
        migrations.AddField(
            model_name='user_level',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user_level',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
