from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from wx_sm_app.utils import *
from .serializers import UserMessageSerrializer
from django.forms.models import model_to_dict
from rest_framework.response import Response
from wx_sm_app.baseresponse import BaseResponse
from .models import UserMessage

class GetMyMessages(APIView):
    @check_login
    def get(self, request, openid):
        try:
            userid = UserInfo.objects.filter(openId=openid).first().userid
            myMessages = UserMessage.objects.filter(receiveId=userid).all().order_by('-create_time')
            message_Page = Message_Page()  # 实例化分页器，
            page_message_list = message_Page.paginate_queryset(queryset=myMessages, request=request,
                                                               view=self)  # 把数据放在分页器上面
            serializer = UserMessageSerrializer(instance=page_message_list, many=True)  # 序列化数据
            res = BaseResponse(code='1043', msg='获取我的消息列表成功',
                               data=serializer.data)
            res.next = message_Page.get_next_link()
            return Response(res.result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='1413', msg='获取我的消息列表失败，请稍后再试').result)



