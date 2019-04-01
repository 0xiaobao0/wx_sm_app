# coding=utf-8
from django.forms.models import model_to_dict
from .models import UserInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from wx_sm_app.baseresponse import BaseResponse
from wx_sm_app.utils import check_login
import json
# Create your views here.


class GetuserInfo(APIView):
    @check_login
    def post(self, request, openid):
        # 尝试获取名为rawData的表单，该表单为小程序向微信服务器请求得到的用户最新信息，
        # 并用token中的openid在用户数据库中找当前登录用户
        try:
            rawData = json.loads(request.POST.get('rawData', ''))
            user = UserInfo.objects.filter(openId=openid).first()
            if ( user== None):  #获取表单成功，没有找到这个用户的数据，则该用户为新用户，将其信息保存
                userinfo = UserInfo(openId=openid, nickName=rawData['nickName'], gender=rawData['gender'],
                                    city=rawData['city'], avatarUrl=rawData['avatarUrl'])
                userinfo.save()
                user_data = model_to_dict(UserInfo.objects.get(openId=openid))
                return Response(BaseResponse(code='1001', msg='保存用户信息成功', data=user_data).result)
            else:   #获取表单成功，并且找到了这个用户的数据
                user_new_data = {'openId': openid, 'nickName': rawData['nickName'], 'gender': rawData['gender'],
                                    'city': rawData['city'], 'avatarUrl': rawData['avatarUrl']}
                user_data = model_to_dict(UserInfo.objects.get(openId=openid))
                user_data.pop('userid')
                user_message = model_to_dict(UserInfo.objects.get(openId=openid))
                if(user_data != user_new_data): #如果原信息不等于新信息，则修更新数据库中的信息，并返回
                    UserInfo.objects.filter(openId=openid).update(nickName=rawData['nickName'], gender=rawData['gender'],
                                    city=rawData['city'], avatarUrl=rawData['avatarUrl'])
                    return Response(BaseResponse(code='1403', msg='修改用户信息成功', data=model_to_dict(UserInfo.objects.get(openId=openid))).result)
                else:   #如果原信息等于新信息，则直接返回用户信息
                    return Response(BaseResponse(code='1403', msg='获取用户信息成功', data=user_message).result)
        except Exception as e:  #获取表单内容失败，无法执行查询
            print(e)
            return Response(BaseResponse(code='1404', msg='获取用户信息失败').result)