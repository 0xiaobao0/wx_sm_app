from django.shortcuts import render
import traceback
from rest_framework.views import APIView
from wx_sm_app.utils import *
from django.forms.models import model_to_dict
from .forms import *
from rest_framework.response import Response
from wx_sm_app.baseresponse import BaseResponse
from .serializers import DeclareSerializer, ArticalSerrializer, CommentSerrializer
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from message.models import UserMessage

# Create your views here.

class Topic(APIView):
    @auth_admin
    def post(self,request, openid):
        try:
            new_topic_querydict = post_querydict_append_sender(request, openid, senderFiled='sender')
            topic_form = TopicForm(new_topic_querydict)
            topic_model_form = TopicModelForm(new_topic_querydict)
            valid = topic_form.is_valid()
            if valid == True:
                topic_model_form.save()
                return Response(BaseResponse(code='200', msg='话题提交成功',
                                             data=model_to_dict(TopicProfile.objects.last())).result)
            else:
                return Response(BaseResponse(code='403', msg='请按照格式填写必须字段后再次提交').result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='发布过程出现意外，请稍后再试').result)

    # @check_login
    def get(self, request):
        import time
        try:
            topicObj = TopicProfile.objects.last()
            startTimeStr = topicObj.start_time + ' 00:00:00'
            endTimeStr = topicObj.end_time + ' 00:00:00'
            startTimeArray = time.strptime(startTimeStr, "%Y-%m-%d %H:%M:%S")
            endTimeArray = time.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S")
            topicObj.start_time = int(time.mktime(startTimeArray))
            topicObj.end_time = int(time.mktime(endTimeArray))
            return Response(BaseResponse(code='200', msg='获取话题成功', data=model_to_dict(topicObj)).result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='获取话题失败').result)




class ArticleFever(APIView):
    @check_login
    def post(self, request, openid):
        try:
            articalId = request.POST.get('articalId', '')
            key = '{}+'.format(articalId)
            print(key)
            if(cache.get(key)):
                value = cache.get(key) + 1
                cache.set(key, value, 60*60*24*365)
            else:
                cache.set(key, 1, 60*60*24*365)
            return Response(BaseResponse(code='200', msg='文章热度+1').result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='文章热度增加失败').result)

class Like(APIView):
    @check_login
    def post(self, request, openid):
        try:
            userId = UserInfo.objects.filter(openId=openid).first().userid
            userMessage = model_to_dict(UserInfo.objects.get(openId=openid))
            articalId = request.POST.get('articalId')
            articalMessage = model_to_dict(ArticalProfile.objects.get(declareid=int(articalId)))
            articalAuthorId = ArticalProfile.objects.filter(declareid=int(articalId)).first().sender.userid
            likeState = request.POST.get('likeState')
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            key = "{}=>{}".format(userId, articalId)
            print(key)
            value = likeState
            cache.set(key, value, 60*60*24*365)

            if(likeState == '1'):
                message = UserMessage(senderId_id=userId, receiveId_id=articalAuthorId,messageType='like_message',
                                      message='收到一条点赞', messageRelate=articalMessage)
                message.save()
                message_dict = model_to_dict(UserMessage.objects.filter(receiveId_id=articalAuthorId).last())
                message_dict['type'] = 'user_message'
                message_dict['message_type'] = 'like_message'
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.send)(
                    str(articalAuthorId),
                    message_dict
                )
                return Response(BaseResponse(code='200', msg='点赞成功', data={key: likeState}).result)
            else:
                if(cache.has_key(key)):
                    cache.delete_pattern(key)
                    return Response(BaseResponse(code='200', msg='取消点赞成功', data={key: likeState}).result)


        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='点赞失败，请稍后再试').result)

    @check_login
    def get(self, request, openid):
        try:
            userId = UserInfo.objects.filter(openId=openid).first().userid
            cacheKeys = "{}=>{}".format(userId, '*')
            keys = cache.keys(cacheKeys)
            articalId = [int(i.split('>')[1]) for i in keys]
            return Response(BaseResponse(code='200', msg='获取用户点赞信息成功', data=articalId).result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='获取用户点赞信息失败，请稍后再试').result)


class GetMyArticalList(APIView):
    @check_login
    def get(self, request, openid):
        try:
            userid = UserInfo.objects.filter(openId=openid).first().userid
            myMessages = ArticalProfile.objects.filter(sender=userid, adopt=1).all().order_by('-create_time')
            message_Page = Message_Page()  # 实例化分页器，
            page_message_list = message_Page.paginate_queryset(queryset=myMessages, request=request,
                                                               view=self)  # 把数据放在分页器上面
            serializer = ArticalSerrializer(instance=page_message_list, many=True)  # 序列化数据
            res = BaseResponse(code='200', msg='获取我的文章列表成功',
                               data=serializer.data)
            res.next = message_Page.get_next_link()
            return Response(res.result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='获取我的文章列表失败，请稍后再试').result)

class GetArticalList(APIView):
    # @check_login
    def get(self, request):
        try:
            messages = ArticalProfile.objects.filter(adopt=1).all().order_by('-create_time')  # 找到所有的数据项
            message_Page = Message_Page()  # 实例化分页器，
            page_message_list = message_Page.paginate_queryset(queryset=messages, request=request, view=self)  # 把数据放在分页器上面
            serializer = ArticalSerrializer(instance=page_message_list, many=True)  # 序列化数据
            res = BaseResponse(code='200', msg='获取文章列表成功',
                                         data=serializer.data)
            res.next = message_Page.get_next_link()
            return Response(res.result)
        except Exception as e:
            traceback.print_exc()
            return Response(BaseResponse(code='500', msg='获取文章列表失败，请稍后再试').result)


class PostArtical(APIView):
    @check_login
    def post(self, request, openid):
        try:
            new_artical_querydict = post_querydict_append_sender(request, openid, senderFiled='sender')
            artical_form = ArticalForm(new_artical_querydict)
            artical_model_form = ArticalModelForm(new_artical_querydict)
            valid = artical_form.is_valid()
            if valid == True:
                artical_model_form.save()
                return Response(BaseResponse(code='200', msg='文章发表成功',
                                             data=model_to_dict(ArticalProfile.objects.last())).result)
            else:
                return Response(BaseResponse(code='403', msg='请填写必须字段后发表').result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='发布过程出现意外，请稍后再试').result)


class PostDeclare(APIView):
    @check_login
    def post(self, request, openid):
        try:
            new_declare_querydict = post_querydict_append_sender(request, openid, senderFiled='sender')
            declare_form = DeclareForm(new_declare_querydict)
            declare_model_form = DeclareModelForm(new_declare_querydict)
            valid = declare_form.is_valid()
            if valid == True:
                declare_model_form.save()
                return Response(BaseResponse(code='200', msg='表白发表成功',
                                             data=model_to_dict(DeclareProfile.objects.last())).result)
            else:
                return Response(BaseResponse(code='403', msg='请填写必须字段后发表').result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='发布过程出现意外，请稍后再试').result)

# 文章评论
class PostComment(APIView):
    @check_login
    def post(self, request, openid):
        # 尝试获取评论表单，并将评论保存至对应文章的评论表
        try:
            new_comment_querydict = post_querydict_append_sender(request, openid, senderFiled='sender')
            comment_form = ArticalCommentForm(new_comment_querydict)
            comment_model_form = ArticalCommentModelForm(new_comment_querydict)

            valid = comment_form.is_valid()
            if valid == True:
                comment_model_form.save()
                result = BaseResponse(code='200', msg='评论发表成功',
                                      data=model_to_dict(ArticalCommentProfile.objects.last())).result
                return Response(result)
            else:
                return Response(BaseResponse(code='403', msg='请填写必须字段后发表').result)

        #失败时执行下面操作
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='评论失败，请稍后再试').result)

class GetComment(APIView):
    def post(self, request):
        articalId = request.POST.get('articalId')
        comment = ArticalCommentProfile.objects.filter(belong_to=articalId, adopt=1).all().order_by('create_time')
        message_Page = Message_Page()  # 实例化分页器，
        page_message_list = message_Page.paginate_queryset(queryset=comment, request=request,
                                                           view=self)  # 把数据放在分页器上面
        serializer = CommentSerrializer(instance=page_message_list, many=True)  # 序列化数据
        res = BaseResponse(code='200', msg='获取文章评论成功',
                           data=serializer.data)
        res.next = message_Page.get_next_link()
        return Response(res.result)




# 1410为发表文章异常，1430为评论发表异常


