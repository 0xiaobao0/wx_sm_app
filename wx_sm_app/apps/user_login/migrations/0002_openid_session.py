# Generated by Django 2.1.4 on 2019-01-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Openid_Session',
            fields=[
                ('openId', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='openid')),
                ('session_key', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='session_key')),
            ],
            options={
                'verbose_name': 'openid和session_key',
                'verbose_name_plural': 'openid和session_key',
            },
        ),
    ]
