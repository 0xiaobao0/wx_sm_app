# coding=utf-8
from django.forms.models import model_to_dict
from .models import UserInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from wx_sm_app.baseresponse import BaseResponse
from wx_sm_app.utils import check_login
import json
# Create your views here.
class Regist(APIView):
    @check_login
    def post(self, request, openid):
        try:
            rawData = json.loads(request.POST.get('rawData', ''))
            user = UserInfo.objects.filter(openId=openid).first()
            if(user == None):
                userinfo = UserInfo(openId=openid, nickName=rawData['nickName'], gender=rawData['gender'],
                                    city=rawData['city'], avatarUrl=rawData['avatarUrl'])
                userinfo.save()
                user_data = model_to_dict(UserInfo.objects.get(openId=openid))
                user_data.pop('userid')
                user_data.pop('openId')
                return Response(BaseResponse(code='400', msg='用户注册成功', data=user_data).result)
            else:
                return Response(BaseResponse(code='403', msg='用户已存在').result)

        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='用户注册失败').result)

class ChangeUserInfo(APIView):
    @check_login
    def post(self, request, openid):
        try:
            nickName = request.POST.get('nickName', '')
            gender = request.POST.get('gender', '')
            avatarUrl = request.POST.get('avatarUrl', '')
            college_and_major = request.POST.get('college_and_major', '')
            studentId = request.POST.get('studentId', '')
            age = request.POST.get('age', '')
            if(nickName != ''):
                UserInfo.objects.filter(openId=openid).update(nickName=nickName)
            if (gender != ''):
                UserInfo.objects.filter(openId=openid).update(gender=gender)
            if (avatarUrl != ''):
                UserInfo.objects.filter(openId=openid).update(avatarUrl=avatarUrl)
            if (college_and_major != ''):
                UserInfo.objects.filter(openId=openid).update(major=college_and_major)
            if (avatarUrl != ''):
                UserInfo.objects.filter(openId=openid).update(studentId=studentId)
            if (age != ''):
                UserInfo.objects.filter(openId=openid).update(age=age)
            user_data = model_to_dict(UserInfo.objects.get(openId=openid))
            user_data.pop('userid')
            user_data.pop('openId')
            return Response(BaseResponse(code='200', msg='修改用户信息成功', data=user_data).result)

        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='修改用户信息失败').result)



class GetuserInfo(APIView):
    @check_login
    def get(self, request, openid):
        try:
            user_data = model_to_dict(UserInfo.objects.get(openId=openid))
            user_data.pop('userid')
            user_data.pop('openId')
            return Response(BaseResponse(code='200', msg='获取用户信息成功', data=user_data).result)
        except Exception as e:
            print(e)
            not_found = ('UserInfo matching query does not exist.',)
            if(e.args == not_found):
                # 该用户为新用户
                return Response(BaseResponse(code='403', msg='用户尚未注册').result)
            else:
                return Response(BaseResponse(code='403', msg='获取用户信息出错').result)

