# coding=utf-8
from django import forms
from .models import *
__author__ = 'wangchuan'
__date__ = '2019/1/22 11:39'

class MessageForm(forms.Form):
    senderId = forms.IntegerField(required=True)
    receiveId = forms.IntegerField(required=True)
    messageType = forms.CharField(required=True)
    messageObj = forms.CharField(required=True)
    messageRelate = forms.CharField(required=True)



class MessageModelForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = '__all__'
        exclude = ['create_time']

