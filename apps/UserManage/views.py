#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from models import UserRole,UserInfo
from forms import LoginUserForm, AddUserForm, EditUserForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import utils

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
@login_required
def LogoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required
@utils.role_required(['superuser'])
def UserMain(request):
    rolename = utils.get_rolename_by_username(request.user)
    return_dict = {'rolename':rolename, 'username':request.user, 'errorwindowname':'None'}
    
    #add user
    adduserform = AddUserForm()
    return_dict['addUserForm'] = adduserform
    
    edituserform = EditUserForm()
    return_dict['editUserForm'] = edituserform
    
    if request.method == "POST":
        if request.POST.get('formtype') == 'add':
            adduserform = AddUserForm(request.POST)
            if adduserform.is_valid():
                
                user = User.objects.create_user(adduserform.fields.get('username'), 
                                                adduserform.fields.get('email'),
                                                adduserform.fields.get('password'))
                userrole = UserRole(username=user.username, 
                                    rolename=adduserform.fields.get('rolename'),
                                    domain=adduserform.fields.get('domain'),
                                    realname=adduserform.fields.get('realname'))
                user.save()
                userrole.save()
                
            else:
                return_dict['errorwindowname'] = 'messagewindow'
                return_dict['errormessage'] = adduserform.error_message
                
        if request.POST.get('formtype') == 'edit':
            pass
            
        if request.POST.get('formtype') == 'delete':
            pass

    #list user
    users = User.objects.all()
    userinfos = []
    for user in users:
        userinfos.append(UserInfo(user))
    
    return_dict['userlist'] = userinfos
    
    return render_to_response('UserManage/user.html',return_dict, RequestContext(request))


@login_required
@utils.role_required(['superuser'])
def ListUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
@utils.role_required(['superuser'])
def EditUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
@utils.role_required(['superuser'])
def DeleteUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
def ChangePassword(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
def ResetPassword(request):
    return HttpResponse(sys._getframe().f_code.co_name)
