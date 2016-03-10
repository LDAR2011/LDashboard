#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserRole(models.Model):
    Roles = ['superuser', 'comptoller', 'commonuser']
    domains = []
    username = models.CharField(max_length=200)
    rolename = models.CharField(max_length=60)
    domain = models.CharField(max_length=200)
    realname = models.CharField(max_length=200)
    def __str__(self):
        return '('+self.username+','+self.rolename+','+self.domain+','+self.realname+')'
        

class UserInfo:
    def __init__(self, user):
        try:
            userrole = UserRole.objects.get(username=user.username)
        except Exception as e:
            self.rolename = 'unknown'
            self.domain = 'unknown'
            self.realname = 'unknown'
        else:
            self.rolename = userrole.rolename
            self.domain = userrole.domain
            self.realname = userrole.realname
        self.username = user.username
        self.email = user.email
        
        
        
        