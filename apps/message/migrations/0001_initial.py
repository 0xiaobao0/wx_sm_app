# Generated by Django 2.1.4 on 2019-05-22 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('getuserinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('messageId', models.AutoField(primary_key=True, serialize=False, verbose_name='消息id')),
                ('messageType', models.CharField(blank=True, default=None, max_length=15, null=True, verbose_name='消息类型')),
                ('messageObj', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='消息主体')),
                ('messageRelate', models.CharField(blank=True, default='', max_length=5000, null=True, verbose_name='消息涉及对象')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('receiveId', models.ForeignKey(blank=True, default='', null=True, on_delete=None, related_name='receiver', to='getuserinfo.UserInfo', verbose_name='接收者id')),
                ('senderId', models.ForeignKey(blank=True, default='', null=True, on_delete=None, related_name='sender', to='getuserinfo.UserInfo', verbose_name='发送者id')),
            ],
            options={
                'verbose_name': '消息表',
                'verbose_name_plural': '消息表',
            },
        ),
    ]