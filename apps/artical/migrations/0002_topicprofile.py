# Generated by Django 2.1.4 on 2019-06-03 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artical', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='话题标题')),
                ('content', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='话题内容')),
                ('start_time', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='话题开始时间')),
                ('end_time', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='话题结束时间')),
            ],
            options={
                'verbose_name': '话题',
                'verbose_name_plural': '话题',
            },
        ),
    ]
