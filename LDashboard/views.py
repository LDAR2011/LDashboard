
from django.http import HttpResponse
import sys
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response,RequestContext
from apps.UserManage.models import UserRole

@login_required
def home(request):
    return render_to_response('index.html',locals(),RequestContext(request))
    