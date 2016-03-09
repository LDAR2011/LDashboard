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
            if rolename in required_role:
                return f(request, *args)
            else:
                return HttpResponseRedirect(reverse('loginurl'))
            
        return wrapped_f
    return wrap
    
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
    
    if user.is_superuser:
        return 'superuser'
    
    try:
        userrole = UserRole.objects.get(username=username)
    except Exception as e:
        return ''
    
    return userrole.rolename
    
    