"""wx_sm_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_login.views import UserLogin, VerifyToken
from getuserinfo.views import GetuserInfo, Regist, ChangeUserInfo
from artical.views import PostDeclare, PostArtical, PostComment, GetComment, GetArticalList, GetMyArticalList, Like, ArticleFever, Topic
from message.views import GetMyMessages
from school_service.views import BindStudentId, GetGlass, GetClassDesign, GetPreWeek, GetExperiment, GetEmptyClassroom
from get_qiniu_token.views import GetQiniuToken

import xadmin

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # path('admin/', admin.site.urls),
    path('api/1.0/auth', UserLogin.as_view()),
    path('api/1.0/regist',Regist.as_view()),
    path('api/1.0/get_user_info',GetuserInfo.as_view()),
    path('api/1.0/change_user_info',ChangeUserInfo.as_view()),
    path('api/1.0/artical', PostArtical.as_view()),
    path('api/1.0/declare', PostDeclare.as_view()),
    path('api/1.0/get_upload_token', GetQiniuToken.as_view()),
    path('api/1.0/post_comment', PostComment.as_view()),
    path('api/1.0/get_comment', GetComment.as_view()),
    path('api/1.0/get_artical_list', GetArticalList.as_view()),
    path('api/1.0/get_my_artical_list', GetMyArticalList.as_view()),
    path('api/1.0/like', Like.as_view()),
    path('api/1.0/get_my_message', GetMyMessages.as_view()),
    path('api/1.0/bind_student_id', BindStudentId.as_view()),
    path('api/1.0/get_class', GetGlass.as_view()),
    path('api/1.0/get_classdesign', GetClassDesign.as_view()),
    path('api/1.0/get_pre_week', GetPreWeek.as_view()),
    path('api/1.0/verity_token', VerifyToken.as_view()),
    path('api/1.0/add_article_fever', ArticleFever.as_view()),
    path('api/1.0/get_experiment', GetExperiment.as_view()),
    path('api/1.0/get_empty_classroom', GetEmptyClassroom.as_view()),
    path('api/1.0/topic', Topic.as_view())
]
