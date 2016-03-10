#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model

class LoginUserForm(forms.Form):
    username = forms.CharField(label=u'账 号',error_messages={'required':u'账号不能为空'},
        widget=forms.TextInput(attrs={'class':'form-control top'}))
    password = forms.CharField(label=u'密 码',error_messages={'required':u'密码不能为空'},
        widget=forms.PasswordInput(attrs={'class':'form-control buttom'}))
        
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        
        super(LoginUserForm, self).__init__(*args, **kwargs)
    
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache
        
    
class AddUserForm(forms.Form):
    username = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'class':'form-control form-group', 'placeholder':u'用户名'}),initial='')
    password = forms.CharField(label='',required=False,widget=forms.PasswordInput(attrs={'class':'form-control form-group', 'placeholder':u'密码'}),initial='')
    rpassword = forms.CharField(label='',required=False,widget=forms.PasswordInput(attrs={'class':'form-control form-group', 'placeholder':u'确认密码'}),initial='')
    rolename = forms.ChoiceField(label='',required=False,choices=(('superuser', u'超级管理员'), ('comptoller',u'审计员'), ('commonuser',u'普通用户')), 
        widget=forms.Select(attrs={'class':'form-control form-group'}), initial='commonuser')
    domain = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'class':'form-control form-group', 'placeholder':u'用户域'}),initial='')
    realname = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'class':'form-control form-group', 'placeholder':u'姓名'}),initial='')
    email = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'class':'form-control form-group', 'placeholder':u'邮箱'}),initial='')    
    
    def __init__(self,*args, **kwargs):
        self.error_message = u'添加新用户失败'
        self.fields = {}
        super(AddUserForm,self).__init__(*args,**kwargs)
        
    
    def check_password_strength(self,password):
        import re
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None
        
        if length_error:
            self.error_message += u',密码长度要至少8位'
            return self.error_message
        if digit_error or uppercase_error or lowercase_error:
            self.error_message += u',密码必须同时包含大写字母、小写字母和数字'
            return self.error_message
        
        return 'ok'
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        self.fields['username'] = username
    
        if not username:
            self.error_message += u',用户名不能为空'
            raise forms.ValidationError(self.error_message)
        return self.cleaned_data
        
    def clean_password(self):
        self.fields['password'] = self.cleaned_data.get('password')
        return self.cleaned_data
    
    def clean_rolename(self):
        self.fields['rolename'] = self.cleaned_data.get('rolename')
        return self.cleaned_data
    
    def clean_domain(self):
        self.fields['domain'] = self.cleaned_data.get('domain')
        return self.cleaned_data
    
    def clean_realname(self):
        self.fields['realname'] = self.cleaned_data.get('realname')
        return self.cleaned_data
    
    def clean_email(self):
        self.fields['email'] = self.cleaned_data.get('email')
        return self.cleaned_data
    
    def clean_rpassword(self):
        rpassword = self.cleaned_data.get('rpassword')
        self.fields['rpassword'] = rpassword
        
        if not self.fields['password']:
            self.error_message += u',密码不能为空'
            raise forms.ValidationError(self.error_message)
        
        if not self.fields['rpassword']:
            self.error_message += u',重复的密码不能为空'
            raise forms.ValidationError(self.error_message)
            
        if self.check_password_strength(self.fields['password']) != 'ok':
            raise forms.ValidationError(self.error_message)
        
        if self.fields['password'] != self.fields['rpassword']:
            self.error_message += u',两次输入的密码不一致'
            raise forms.ValidationError(self.error_message)
            
        return self.cleaned_data
        
class EditUserForm(forms.Form):
    username = forms.CharField(label='',required=False,widget=forms.TextInput(
        attrs={'class':'form-control form-group', 'placeholder':u'用户名', 'readonly':'True'}),initial='')
    rolename = forms.ChoiceField(label='',required=False,choices=(('superuser', u'超级管理员'), ('comptoller',u'审计员'), ('commonuser',u'普通用户')), 
        widget=forms.Select(attrs={'class':'form-control form-group'}), initial='commonuser')
    domain = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'class':'form-control form-group', 'placeholder':u'用户域'}),initial='')
    realname = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'class':'form-control form-group', 'placeholder':u'姓名'}),initial='')
    email = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'class':'form-control form-group', 'placeholder':u'邮箱'}),initial='')

            
    
        