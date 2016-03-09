from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserRole(models.Model):
    username = models.CharField(max_length=200)
    rolename = models.CharField(max_length=60)
    def __str__(self):
        return self.username+':'+self.rolename