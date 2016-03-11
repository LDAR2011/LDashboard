#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from models import UserRole
#required_role is a list
def role_required(required_role):
    '''
    usage:
    @role_require(['user','superuser'])
    @role_require(['user'])
    '''
    def wrap(f):
        def wrapped_f(request, *args):
            
            rolename = get_rolename_by_username(request.user)
            print rolename
            if rolename in required_role:
                return f(request, *args)
            elif rolename == '':
                userrole = UserRole.objects.get(username=request.user)
                userrole.rolename = u'普通用户'
                userrole.save()
            else:
                return HttpResponseRedirect(reverse('loginurl'))
            
        return wrapped_f
    return wrap

'''
def record_before_clean(fieldname, fields, cleaned_data):
    def wrap(f):
        def wrapped_f(*args):
            fields[fieldname] = cleaned_data.get(fields)
            return f(*args)
        return wrapped_f
    return wrap
'''

def get_rolename_by_username(username):
    '''
    username not exist: Unvalid
    not is_active: Unvalid
    is_superuser: superuser
    
    '''
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        return ''
    
    try:
        userrole = UserRole.objects.get(username=username)
    except Exception as e:
        return ''
    
    return userrole.rolename
    
    