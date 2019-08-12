from rest_framework.response import Response
from rest_framework.views import APIView
from wx_sm_app.utils import check_login
from wx_sm_app.baseresponse import BaseResponse
import qiniu
import uuid


# Create your views here.
class GetQiniuToken(APIView):
    @check_login
    def get(self, request, openid):
        ACCESS_KEY = 'EI5u9AjeOC8Z6E-dO8779gUHFvn2OzZygG6TTaWy'
        SECRET_KEY = 'UhfftOyhvZ4rYYrxVkwkg-KD0Xtf685zTkYZAXz9'
        BUCKET_NAME = '0store0'
        key = str(uuid.uuid1()).replace('-', '')  # 这里使用uuid作为保存在七牛里文件的名字。并去掉了uuid中的“-”
        q = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
        token = q.upload_token(BUCKET_NAME, key, 7200, {
            'returnBody': '{"name": "$(fname)", "key": "$(key)"}',
            'fsizeLimit': 5242880,
            'mimeLimit': 'image/*'
        })
        data = {'token': token, 'key': key}
        result = BaseResponse(code=1020, msg='获取上传token成功', data=data).result
        result['uptoken'] = token
        return Response(result)