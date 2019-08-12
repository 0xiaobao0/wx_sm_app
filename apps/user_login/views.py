from django.shortcuts import render
from .models import Openid_Session
from rest_framework.views import APIView
from rest_framework.response import Response
from wx_sm_app.baseresponse import BaseResponse
from wx_sm_app.utils import generate_jwt
from wx_sm_app import config
from wx_sm_app.utils import check_login
import requests

# Create your views here.

class UserLogin(APIView):
    def post(self, requset):
        receive_code = requset.POST.get('code', '')
        if(receive_code != ''):
            jscode2session = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(APPID=config.APPID, SECRET=config.SECRET, JSCODE=receive_code)
            result = requests.get(jscode2session).json()
            # print(result)
            if 'errmsg' in result.keys():
                return Response(BaseResponse(code='401', msg='用户登录失败').result)
            else:
                openid_session = Openid_Session(openId=result['openid'], session_key=result['session_key'])
                openid_session.save()
                result = generate_jwt(result['openid'])
                return Response(result)

class VerifyToken(APIView):
    @check_login
    def get(self, request, openid):
        if(openid):
            return Response(BaseResponse(code='200', msg='token有效').result)





