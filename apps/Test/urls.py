from django.conf.urls import url,include

import views

#import sys
#import os
#print sys.path
#print os.getcwd()

urlpatterns = [
    url(r'^$', views.index, name='index'),
]


