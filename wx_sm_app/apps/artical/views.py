from django.shortcuts import render
from rest_framework.views import APIView
from wx_sm_app.utils import *
from django.forms.models import model_to_dict
from .forms import *
from rest_framework.response import Response
from wx_sm_app.baseresponse import BaseResponse

# Create your views here.
class PostDeclare(APIView):
    @check_login
    def post(self, request, openid):
        try:
            new_declare_querydict = post_querydict_append_sender(request, openid)
            declare_form = DeclareForm(new_declare_querydict)
            declare_model_form = DeclareModelForm(new_declare_querydict)
            valid = declare_form.is_valid()
            if valid == True:
                declare_model_form.save()
                return Response(BaseResponse(code='1010', msg='发表成功',
                                             data=model_to_dict(DeclareProfile.objects.last())).result)
            else:
                return Response(BaseResponse(code='1410', msg='请填写必须字段后发表').result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='1010', msg='发布过程出现意外，请稍后再试').result)

# 文章评论
class Comment(APIView):
    @check_login
    def post(self, request, openid):
        # 尝试获取评论表单，并将评论保存至对应文章的评论表
        try:
            new_comment_querydict = post_querydict_append_sender(request, openid)
            if(new_comment_querydict.get('comment_type') == 'to_artical'):
                comment_form = ArticalCommentForm(new_comment_querydict)
                comment_model_form = ArticalCommentModelForm(new_comment_querydict)
                result = BaseResponse(code='1030', msg='评论发表成功',
                                             data=new_comment_querydict.get('comment_content')).result
            else:
                comment_form = CommentCommentForm(new_comment_querydict)
                comment_model_form = CommentCommentModelForm(new_comment_querydict)
                result = BaseResponse(code='1030', msg='评论发表成功',
                                      data=new_comment_querydict.get('comment_content')).result
            valid = comment_form.is_valid()
            if valid == True:
                comment_model_form.save()
                return Response(result)
            else:
                return Response(BaseResponse(code='1431', msg='请填写必须字段后发表').result)

        #失败时执行下面操作
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='1430', msg='评论失败，请稍后再试').result)

# 1410为发表文章异常，1430为评论发表异常


