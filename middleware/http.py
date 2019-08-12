# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/5/31 17:20'

from django.utils.deprecation import MiddlewareMixin

class SetRemoteAddrFromForwardedFor(MiddlewareMixin):
    def process_request(self, request):
        # print(request.META)
        # print(request.META['REMOTE_HOST'])
        # request.META['REMOTE_HOST'] = 'asd'
        # request.META['REMOTE_ADDR'] = 'asd'
        try:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
        except:
            pass
        # print(request.META)
        # try:
        #     print(request.META['HTTP_X-Forwarded-For'])
        #     print(request.META['HTTP_X-Real-IP'])
        # except:
        #     pass
        # try:
        #     real_ip = request.META['HTTP_X_FORWARDED_FOR']
        # except:
        #     pass
        # else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            # real_ip = real_ip.split(",")[0]
