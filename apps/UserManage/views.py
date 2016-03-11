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

from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

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
@utils.role_required([u'超级管理员'])
def UserMain(request):
    rolename = utils.get_rolename_by_username(request.user)
    return_dict = {'rolename':rolename, 'username':request.user, 'windowname':'None'}
    
    #add user
    adduserform = AddUserForm()
    return_dict['addUserForm'] = adduserform
    
    edituserform = EditUserForm()
    return_dict['editUserForm'] = edituserform
    
    if request.method == "POST":
        if request.POST.get('formtype') == 'add':
            adduserform = AddUserForm(request.POST)
            if adduserform.is_valid():
                
                if User.objects.filter(username=adduserform.fields.get('username')).count() == 0:
                    
                    user = User.objects.create_user(adduserform.fields.get('username'), adduserform.fields.get('email'),\
                            adduserform.fields.get('password'))
                    user.save()
                    userrole_list = UserRole.objects.filter(username=adduserform.fields.get('username'))
                    if userrole_list.count() != 0:
                        userrole_list.delete()
                    
                    userrole = UserRole(username=user.username, rolename=adduserform.fields.get('rolename'),\
                                domain=adduserform.fields.get('domain'),realname=adduserform.fields.get('realname'))                    
                    userrole.save()
                    
                    return_dict['windowname'] = 'successwindow'
                    return_dict['windowmessage'] = u'增加用户成功'
                    
                else:
                    return_dict['windowname'] = 'errorwindow'
                    return_dict['windowmessage'] = u'用户名已存在，请更换用户名'
                    
            else:
                return_dict['windowname'] = 'errorwindow'
                return_dict['windowmessage'] = adduserform.error_message
                
        if request.POST.get('formtype') == 'edit':
            edituserform = EditUserForm(request.POST)
            if edituserform.is_valid():
                
                user = User.objects.get(username=edituserform.fields.get('username'))
                userrole = UserRole.objects.get(username=edituserform.fields.get('username'))
                
                user.email = edituserform.fields.get('email')
                userrole.rolename, userrole.domain, userrole.realname = \
                    edituserform.fields.get('rolename'),edituserform.fields.get('domain'),edituserform.fields.get('realname')
                
                user.save()
                userrole.save()
                
                return_dict['windowname'] = 'successwindow'
                return_dict['windowmessage'] = u'修改用户属性成功'
                
            else:
                return_dict['windowname'] = 'errorwindow'
                return_dict['windowmessage'] = edituserform.error_message
                
        if request.POST.get('formtype') == 'delete':
            
            deleteusername = request.POST.get('username','')
            print 'deleteusername:',deleteusername
            if deleteusername == request.user:
                return_dict['windowname'] = 'errorwindow'
                return_dict['windowmessage'] = u'不能删除自己'
            
            User.objects.filter(username=deleteusername).delete()
            UserRole.objects.filter(username=deleteusername).delete()
            
            return_dict['windowname'] = 'successwindow'
            return_dict['windowmessage'] = u'删除用户成功'

    #list user
    users = User.objects.all()
    userinfos = []
    for user in users:
        userinfos.append(UserInfo(user))
    
    
    paginator = Paginator(userinfos, 25)
    
    try:
        page = request.GET.get('page','1')
        userinfos = paginator.page(page)
    except PageNotAnInteger:
        userinfos = paginator.page(1)
    except EmptyPage:
        userinfos = paginator.page(paginator.num_pages)
    except Exception:
        userinfos = paginator.page(1)
        
    
    return_dict['userlist'] = userinfos
    print userinfos.number
    
    return render_to_response('UserManage/user.html',return_dict, RequestContext(request))


@login_required
@utils.role_required([u'超级管理员'])
def ListUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
@utils.role_required([u'超级管理员'])
def EditUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
@utils.role_required([u'超级管理员'])
def DeleteUser(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
def ChangePassword(request):
    return HttpResponse(sys._getframe().f_code.co_name)

@login_required
def ResetPassword(request):
    return HttpResponse(sys._getframe().f_code.co_name)
