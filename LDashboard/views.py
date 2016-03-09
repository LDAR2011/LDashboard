
from django.http import HttpResponse
import sys
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response,RequestContext
from apps.UserManage.models import UserRole
from apps.UserManage.utils import role_required,get_rolename_by_username


@login_required
def home(request):
    rolename = get_rolename_by_username(request.user)
    return render_to_response('index.html',{'rolename':rolename, 'username':request.user},RequestContext(request))
    


#404 page
def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    print 'here'
    response.status_code = 404
    return response
    