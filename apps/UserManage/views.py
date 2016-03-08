#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from models import UserRole
from forms import LoginUserForm
from django.contrib import auth

'''
url(r'^user/add/$', views.AddUser, name='adduserurl'),
url(r'^user/list/$', views.ListUser, name='listuserurl'),
url(r'^user/edit/(?P<ID>\d+)/$', views.EditUser, name='edituserurl'),
url(r'^user/delete/(?P<ID>\d+)/$', views.DeleteUser, name='deleteuserurl'),
url(r'^user/changepwd/$', views.ChangePassword, name='changepasswordurl'),
url(r'^user/resetpwd/(?P<ID>\d+)/$', views.ResetPassword, name='resetpasswordurl'),
'''
import sys

# Create your views here.

#accounts/login
def LoginUser(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
        
    if request.method == 'GET' and request.GET.has_key('next'):
        next = request.GET['next']
    else:
        next = '/'

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST.get('next','/'))
    else:
        form = LoginUserForm(request)

    kwvars = {
        'request':request,
        'form':form,
        'next':next,
    }

    return render_to_response('UserManage/login.html',kwvars,RequestContext(request))

#accounts/logout
def LogoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def AddUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

def ListUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

def EditUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

def DeleteUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

def ChangePassword(request):
    return HttpResponse(sys._getframe().f_code.co_name)

def ResetPassword(request):
    return HttpResponse(sys._getframe().f_code.co_name)
