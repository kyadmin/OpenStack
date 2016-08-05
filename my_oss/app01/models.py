from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class AuthUser(models.Model):
    username=models.OneToOneField(User)
    email=models.EmailField(blank=True,verbose_name='e-mail')
    def __unicode__(self):
        return '%s(%s)' % (self.username,self.email)