from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserRole(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=200)
    role_name = models.CharField(max_length=40)
    