from django.shortcuts import render
from rest_framework.views import APIView
from wx_sm_app.utils import *
# from .serializers import UserMessageSerrializer
from django.forms.models import model_to_dict
from rest_framework.response import Response
from wx_sm_app.baseresponse import BaseResponse
from getuserinfo.models import UserInfo
from django.core.cache import cache

import requests
import base64
import rsa
import json
import time
import re
from bs4 import BeautifulSoup as bs
# from .models import UserMessage



# Create your views here.
class BindStudentId(APIView):
    @check_login
    def post(self, request, openid):
        try:
            self.session = requests.Session()
            userId = UserInfo.objects.filter(openId=openid).first().userid
            self.url = 'http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_slogin.html'
            studentId = request.POST.get('studentId', '')
            password = bytes(request.POST.get('password', ''), encoding='utf-8')
            csrfToken = self.get_csrf_token()
            ncrypted_passwd = self.get_encrypted_passwd(password)

            postdata = {'csrftoken': csrfToken, 'yhm': studentId, 'mm': ncrypted_passwd}
            self.session.post(self.url,data=postdata)
            test_login_url = 'http://jwxt.neuq.edu.cn/jwglxt/xtgl/index_initMenu.html'
            response = self.session.get(url=test_login_url, allow_redirects=False)
            statue = response.status_code
            if(statue == 200):
                UserInfo.objects.filter(openId=openid).update(studentId=studentId)
                print('登陆成功！')
                cookies = 'JSESSIONID='+self.session.cookies._cookies['jwxt.neuq.edu.cn']['/jwglxt/']['JSESSIONID'].value
                key = "{}:{}".format(userId, 'cookies')
                cache.set(key, cookies, 60 * 60 * 24 * 7)
                return Response(BaseResponse(code='200', msg='绑定学号成功').result)
            else:
                return Response(BaseResponse(code='403', msg='绑定学号失败，请稍后再试').result)
        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='绑定学号失败，请稍后再试').result)


    def get_csrf_token(self):
        page = self.session.get(self.url)
        soup = bs(page.text, "html.parser")
        # 获取认证口令csrftoken
        csrftoken = soup.find(id="csrftoken").get("value")
        return csrftoken

    def get_encrypted_passwd(self, password):
        publickey = self.session.get('http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_getPublicKey.html').json()
        b_modulus = base64.b64decode(publickey['modulus'])  # 将base64解码转为bytes
        b_exponent = base64.b64decode(publickey['exponent'])  # 将base64解码转为bytes
        # 公钥生成,python3从bytes中获取int:int.from_bytes(bstring,'big')
        modulus = int.from_bytes(b_modulus, 'big')
        exponent = int.from_bytes(b_exponent, 'big')
        mm_key = rsa.PublicKey(modulus, exponent)
        # 利用公钥加密,bytes转为base64编码
        passwd = base64.b64encode(rsa.encrypt(password, mm_key))
        return passwd

class GetGlass(APIView):
    @check_login
    def get(self, request, openid):
        try:
            self.session = requests.Session()
            userId = UserInfo.objects.filter(openId=openid).first().userid
            classList = []
            num_dict = {'星期一': 1, '星期二': 2, '星期三': 3, '星期四': 4, '星期五': 5, '星期六': 6, '星期日': 7}
            key = "{}:{}".format(userId, 'cookies')
            cookies = cache.get(key)
            xskb_url = 'http://jwxt.neuq.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
            xskb_data = {
                'xnm': '2018',
                'xqm': '12'
            }
            header = {
                "Cookie": cookies
            }
            try:
                xskb_results = self.session.post(xskb_url, data=xskb_data, headers=header).json()
            except:
                return Response(BaseResponse(code='500', msg='登录失效，请重试').result)
            print('课表获取成功')
            for i in xskb_results["kbList"]:
                classObj = {}
                class_range = [int(i) for i in re.findall(r'\d+', i['jc'])]
                week_range = []
                str_week_range = [i for i in re.findall(r'\d+\-?\d*', i['zcd'])]
                for j in str_week_range:
                    rangelist = [int(n) for n in re.findall(r'\d+', j)]
                    week_range.append(rangelist)
                kcmc = i['kcmc'] + '@' + i['cdmc']
                classObj['xqj'] = num_dict[i['xqjmc']]
                classObj['skjc'] = class_range[0]
                classObj['skcd'] = class_range[1] - class_range[0] + 1
                classObj['kcmc'] = kcmc
                classObj['week_range'] = week_range
                classObj['teacher'] = i['xm']
                classObj['test_type'] = i['khfsmc']
                classList.append(classObj)
            # print(classList)
            return Response(BaseResponse(code='200', msg='获取课表成功', data=classList).result)
            #     # print(i['xqjmc'], i['jc'], i['kcmc'] + '@' + i['cdmc'], i['zcd'], i['khfsmc'], i['xm'])
            # print('实践课如下')
            # for i in xskb_results["sjkList"]:
            #     print(i['kcmc'], i['qsjsz'], i['xm'])
            #
            # syk_result = self.session.post(url=syk_url, data=syk_data).json()
            # print('实验课如下')
            # for i in syk_result["items"]:
            #     print(i['jsxm'], i['kcmc'], i['syfj'], i['syfzmc'], i['xmmc'], i['xqjmc'], i['zcd'])

        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='获取课表信息失败，请稍后再试').result)

class GetClassDesign(APIView):
    @check_login
    def get(self, request, openid):
        try:
            self.session = requests.Session()
            userId = UserInfo.objects.filter(openId=openid).first().userid
            classdesign = []
            key = "{}:{}".format(userId, 'cookies')
            cookies = cache.get(key)
            xskb_url = 'http://jwxt.neuq.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
            xskb_data = {
                'xnm': '2018',
                'xqm': '12'
            }
            header = {
                "Cookie": cookies
            }
            try:
                xskb_results = self.session.post(xskb_url, data=xskb_data, headers=header).json()
            except:
                return Response(BaseResponse(code='500', msg='登录失效，请重试').result)
            for i in xskb_results["sjkList"]:
                classdesignObj = {}
                classdesignObj['kcmc'] = i['kcmc']
                classdesignObj['qsjsz'] = i['qsjsz']
                classdesignObj['xm'] = i['xm']
                classdesign.append(classdesignObj)
                # print(i['kcmc'], i['qsjsz'], i['xm'])
            return Response(BaseResponse(code='200', msg='获取课设成功', data=classdesign).result)

        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='获取课设失败，请稍后再试').result)

class GetExperiment(APIView):
    @check_login
    def get(self, request, openid):
        try:
            self.session = requests.Session()
            userId = UserInfo.objects.filter(openId=openid).first().userid
            classList = []
            num_dict = {'星期一': 1, '星期二': 2, '星期三': 3, '星期四': 4, '星期五': 5, '星期六': 6, '星期日': 7}
            key = "{}:{}".format(userId, 'cookies')
            cookies = cache.get(key)
            syk_url = 'http://jwxt.neuq.edu.cn/jwglxt/xssygl/sykbcx_cxSykbcxxsIndex.html?doType=query&gnmkdm=N253508'
            syk_data = {
                'xnm': '2018',
                'xqm': '12'
            }
            header = {
                "Cookie": cookies
            }
            try:
                syk_result = self.session.post(syk_url, data=syk_data, headers=header).json()
            except:
                return Response(BaseResponse(code='500', msg='登录失效，请重试').result)
            print('实验课表获取成功')
            for i in syk_result["items"]:
                classObj = {}
                class_range = [int(i) for i in re.findall(r'\d+', i['jc'])]
                week_range = []
                str_week_range = [i for i in re.findall(r'\d+\-?\d*', i['zcd'])]
                for j in str_week_range:
                    rangelist = [int(n) for n in re.findall(r'\d+', j)]
                    week_range.append(rangelist)
                kcmc = i['kcmc'] + '@' + i['syfj'].split("/")[0]
                classObj['xqj'] = num_dict[i['xqjmc']]
                classObj['skjc'] = class_range[0]
                classObj['skcd'] = class_range[1] - class_range[0] + 1
                classObj['kcmc'] = kcmc
                classObj['week_range'] = week_range
                classObj['teacher'] = i['jsxm']
                classObj['symc'] = i['xmmc']
                classList.append(classObj)
            # print(classList)
            return Response(BaseResponse(code='200', msg='获取实验课表成功', data=classList).result)

        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='获取实验课表信息失败，请稍后再试').result)

class GetEmptyClassroom(APIView):
    @check_login
    def post(self, request, openid):
        try:
            week = request.POST.get('week', '[]')
            day = request.POST.get('day', '[]')
            characters = request.POST.get('characters', '[]')
            print(week, day, characters)
            page = request.POST.get('page', '')
            week_data = str(sum([pow(2,i) for i in json.loads(week)]))
            day_data = ','.join([str(i+1) for i in json.loads(day)])
            characters_data = str(sum([pow(2,i) for i in json.loads(characters)]))

            print(week_data, day_data, characters_data)
            self.session = requests.Session()
            userId = UserInfo.objects.filter(openId=openid).first().userid
            emptyClassroomList = []
            # num_dict = {'星期一': 1, '星期二': 2, '星期三': 3, '星期四': 4, '星期五': 5, '星期六': 6, '星期日': 7}
            key = "{}:{}".format(userId, 'cookies')
            cookies = cache.get(key)
            query_url = 'http://jwxt.neuq.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'
            query_data = {
                'fwzt': 'cx',
                'xnm': '2018',
                'xqm': '12',
                'zcd': week_data,
                'xqj': day_data,
                'jcd': characters_data,
                'jyfs': '0',
                'xqh_id': '3D669E6DAB06A186E053AB14CECA64B4',
                'queryModel.showCount': '15',
                'queryModel.currentPage':str(page),
                'queryModel.sortName': 'cdbh',
                'queryModel.sortOrder': 'asc'
            }
            header = {
                "Cookie": cookies
            }
            try:
                query_result = self.session.post(query_url, data=query_data, headers=header).json()
            except:
                return Response(BaseResponse(code='500', msg='登录失效，请重试').result)
            print('获取空教室成功')
            for i in query_result["items"]:
                emptyClassroomObj = {}
                emptyClassroomObj['cdmc'] = i['cdmc'] #场地名称
                emptyClassroomObj['xqmc'] = i['xqmc'] #校区
                emptyClassroomObj['jxlmc'] = i['jxlmc']  # 楼号
                emptyClassroomObj['zws'] = i['zws']  # 座位数
                emptyClassroomObj['lch'] = i['lch']  # 楼层号
                emptyClassroomObj['cdlbmc'] = i['cdlbmc'] #场地类别

                emptyClassroomList.append(emptyClassroomObj)
            # print(classList)
            return Response(BaseResponse(code='200', msg='获取空教室成功', data=emptyClassroomList).result)

        except Exception as e:
            print(e)
            return Response(BaseResponse(code='500', msg='获取空教室失败，请稍后再试').result)


class GetPreWeek(APIView):
    def get(self, request):
        import time
        # 开学时间，手动维护
        start_year, start_month, start_day = 2019, 3, 4

        now_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
        now_time = now_time.split(".")
        now_year, now_month, now_day = eval(now_time[0]), eval(now_time[1].strip("0")), eval(now_time[2].lstrip("0"))

        if (now_year % 400 == 0) or (now_year % 4 == 0 and now_year % 100 != 0):
            month_year = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            month_year = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if start_year == now_year:
            already_day = (month_year[start_month] - start_day) + sum(month_year[start_month + 1:now_month]) + now_day
            result_week = (already_day // 7) + 1
        else:
            # 上一年总天数
            last_yearday = month_year[start_month] - start_day + sum(month_year[start_month + 1:])
            now_yearday = sum(month_year[0:now_month]) + now_day
            result_week = (last_yearday + now_yearday) // 7 + 1

        return Response(BaseResponse(code='200', msg='当前周为', data=result_week).result)

