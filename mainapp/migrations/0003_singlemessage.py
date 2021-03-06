# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-03-25 18:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_distribution'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f')),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('was_read', 'Was_read'), ('not_sent', 'Not_sent')], default='not_sent', max_length=100)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('distribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Distribution')),
            ],
            options={
                'verbose_name': '\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f',
            },
        ),
    ]
