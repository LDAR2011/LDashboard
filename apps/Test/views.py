from django.shortcuts import render

#import base.sayHello

from base.sayHello import hello

#import sys
#print sys.path

from ..UserManage.models import UserRole

# Create your views here.
def index(request):
    hello()
    return render(request, 'test/index.html', {})