# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/1/2 16:50'

class BaseResponse(object):
    def __init__(self, code=None, msg=None, data=None):
        self.result = {}
        self.result['code'] = code
        self.result['msg'] = msg
        self.result['data'] = data