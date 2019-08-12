# Generated by Django 2.1.4 on 2019-06-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getuserinfo', '0003_auto_20190523_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='管理员姓名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='变更时间')),
                ('userid', models.ForeignKey(blank=True, default='', null=True, on_delete=None, to='getuserinfo.UserInfo', verbose_name='管理员userid')),
            ],
            options={
                'verbose_name': '管理员信息',
                'verbose_name_plural': '管理员信息',
            },
        ),
    ]