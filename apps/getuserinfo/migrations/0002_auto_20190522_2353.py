# Generated by Django 2.1.4 on 2019-05-22 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getuserinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='age',
            field=models.IntegerField(blank=True, default=18, null=True, verbose_name='用户年龄'),
        ),
    ]