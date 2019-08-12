# coding=utf-8
import jwt
import datetime
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination
from wx_sm_app import config
from wx_sm_app import baseresponse
from getuserinfo.models import UserInfo, AdminInfo
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

def auth_admin(func):
    def wrapper(self, request):
        try:
            token = request.META.get('HTTP_TOKEN')
            result = decode_jwt(token)
            if (result['state'] == True):
                Token = result['Token']
                print(Token)
                openid = Token['openid']
                userid = UserInfo.objects.filter(openId=openid).first().userid
                adminUser = AdminInfo.objects.filter(userid=userid).first()
                if (adminUser == None):
                    return Response(BaseResponse(code='1402', msg='该用户无权进行该操作').result)
                else:
                    return func(self, request, openid)
            else:
                return Response(BaseResponse(code='1401', msg='用户认证失败').result)
        except:
            return Response(BaseResponse(code='1402', msg='请先登录').result)
    return wrapper

def generate_jwt(openid):
    datetimeInt = datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24 * 30)
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
def post_querydict_append_sender(request, openid, senderFiled):
    querydict_dict = request.POST
    new_querydict = querydict_dict.copy()
    userid = UserInfo.objects.filter(openId=openid).first().userid
    new_querydict.__setitem__(senderFiled, userid)
    return new_querydict


class Message_Page(LimitOffsetPagination):
    default_limit = 12  # 一页默认几个
    limit_query_param = 'limit'  # 关键字后面跟的是一页显示几个
    offset_query_param = 'offset'  # 这个后面跟的是从哪里显示
    max_limit = 24  # 这个是一页最多显示有几个