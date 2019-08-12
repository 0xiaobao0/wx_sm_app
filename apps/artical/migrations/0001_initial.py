# Generated by Django 2.1.4 on 2019-05-22 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('getuserinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticalCommentProfile',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False, verbose_name='评论id')),
                ('comment_type', models.IntegerField(blank=True, choices=[(0, '对文章的评论'), (1, '对评论的评论')], default=0, null=True, verbose_name='评论类型')),
                ('content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='评论内容')),
                ('comment_to_obj', models.IntegerField(blank=True, default='', null=True, verbose_name='评论对象的id')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论提交时间')),
            ],
            options={
                'verbose_name': '文章评论',
                'verbose_name_plural': '文章评论',
            },
        ),
        migrations.CreateModel(
            name='ArticalProfile',
            fields=[
                ('declareid', models.AutoField(primary_key=True, serialize=False, verbose_name='文章内容id')),
                ('title', models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='文章标题')),
                ('artical', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='内容')),
                ('imgurl', models.CharField(blank=True, default='', max_length=1500, null=True, verbose_name='图片url')),
                ('tag', models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='文章标签')),
                ('public', models.IntegerField(blank=True, choices=[(1, '匿名'), (0, '不匿名')], default=0, null=True, verbose_name='是否匿名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('sender', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='getuserinfo.UserInfo', verbose_name='发送者')),
            ],
            options={
                'verbose_name': '文章信息',
                'verbose_name_plural': '文章信息',
            },
        ),
        migrations.CreateModel(
            name='DeclareProfile',
            fields=[
                ('declareid', models.AutoField(primary_key=True, serialize=False, verbose_name='表白内容id')),
                ('towho', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='接受者')),
                ('anonymous', models.IntegerField(blank=True, choices=[(1, '匿名'), (0, '不匿名')], default=0, null=True, verbose_name='是否匿名')),
                ('imgurl', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='图片url')),
                ('content', models.CharField(blank=True, default='', max_length=5000, null=True, verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('sender', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='getuserinfo.UserInfo', verbose_name='发送者')),
            ],
            options={
                'verbose_name': '表白信息',
                'verbose_name_plural': '表白信息',
            },
        ),
        migrations.AddField(
            model_name='articalcommentprofile',
            name='belong_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='artical.ArticalProfile', verbose_name='评论归属的文章'),
        ),
        migrations.AddField(
            model_name='articalcommentprofile',
            name='sender',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=None, to='getuserinfo.UserInfo', verbose_name='评论发送者'),
        ),
    ]