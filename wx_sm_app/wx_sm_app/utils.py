# coding=utf-8
import jwt
import datetime
from rest_framework.response import Response
from wx_sm_app import config
from wx_sm_app import baseresponse
from getuserinfo.models import UserInfo
import json

__author__ = 'wangchuan'
__date__ = '2019/1/2 16:39'

BaseResponse = baseresponse.BaseResponse

def check_login(func):
    def wrapper(self, request):
        try:
            token = request.META.get('HTTP_TOKEN')
            result = decode_jwt(token)
            if (result['state'] == True):
                Token = result['Token']
                print(Token)
                openid = Token['openid']
                return func(self, request, openid)
            else:
                return Response(BaseResponse(code='1401', msg='用户认证失败').result)
        except:
            return Response(BaseResponse(code='1402', msg='请先登录').result)
    return wrapper


def generate_jwt(openid):
    datetimeInt = datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24 * 7)
    payload = {
        'openid': openid,
        'aud': 'webkit',
        'exp': datetimeInt,  # 过期时间
    }
    token = jwt.encode(payload, config.secret, 'HS256')
    rs = BaseResponse(data={'token': token}, msg='用户登陆成功', code='1000')
    return rs.result


def decode_jwt(token):
    result = {'state': False, 'Token': ''}
    try:
        Token = jwt.decode(token, config.secret, audience='webkit', algorithms=['HS256'])
        result['state'] = True
        result['Token'] = Token
        return result
    except Exception as e:
        print(e)
        return result

# 在表单的querydict对象中加入sender字段
def post_querydict_append_sender(request, openid):
    querydict_dict = request.POST
    new_querydict = querydict_dict.copy()
    userid = UserInfo.objects.filter(openId=openid).first().userid
    new_querydict.__setitem__('sender', userid)
    return new_querydict