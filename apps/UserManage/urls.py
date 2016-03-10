from django.conf.urls import url,include

import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    
    url(r'^login/$', views.LoginUser, name='loginurl'),
    url(r'^logout/$', views.LogoutUser, name='logouturl'),
    
    url(r'^user/$', views.UserMain, name='usermain'),
    
    url(r'^user/changepwd/$', views.ChangePassword, name='changepasswordurl'),
    url(r'^user/resetpwd/(?P<ID>\d+)/$', views.ResetPassword, name='resetpasswordurl'),
    
]