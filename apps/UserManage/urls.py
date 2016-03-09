from django.conf.urls import url,include

import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    
    url(r'^login/$', views.LoginUser, name='loginurl'),
    url(r'^logout/$', views.LogoutUser, name='logouturl'),
    
    url(r'^user/$', views.UserMain, name='usermain'),
    url(r'^user/add/$', views.AddUser, name='adduserurl'),
    url(r'^user/list/$', views.ListUser, name='listuserurl'),
    url(r'^user/edit/(?P<ID>\d+)/$', views.EditUser, name='edituserurl'),
    url(r'^user/delete/(?P<ID>\d+)/$', views.DeleteUser, name='deleteuserurl'),
    
    url(r'^user/changepwd/$', views.ChangePassword, name='changepasswordurl'),
    url(r'^user/resetpwd/(?P<ID>\d+)/$', views.ResetPassword, name='resetpasswordurl'),
    
]