# Create your models here.
from pyexpat import model
from re import M
from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# import jsonfield


class flipping(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    link=models.CharField(max_length=12)
    fname=models.CharField(max_length=40)
    ftime=models.DateTimeField()
    fsub=models.CharField(max_length=20,default=" ")
    upload = models.FileField(upload_to='flipupload', blank=True, null=True)
    times = models.IntegerField(default=0)
    # dates=jsonfield.JSONField(default=list)
    dtime=models.DateTimeField(null=True, blank=True, default=None)
    # dtime stands for disable time, students will lose access to this flipbook after this time
    pages=models.IntegerField(default=0)
    
    def __unicode__(self):
        return '%s' % (self.upload.name)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.upload.name))
        super(flipping,self).delete(*args,**kwargs)

class flipprivacy(models.Model):
    link=models.ForeignKey(flipping,on_delete=models.CASCADE)
    fprivacy=models.CharField(max_length=2, default="b") #no login  required
    # flog=models.CharField(max_length=2) #a2c login required
    fdomain=models.CharField(max_length=10, blank=True, null=True) #domain login required and save the domain name 
    fpass=models.CharField(max_length=10, blank=True, null=True)  #Enter password for the file
    # fpri=models.CharField(max_length=2) #make the file private (access to no one)

class flipcollection(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    fobj=models.ForeignKey(flipping,on_delete=models.CASCADE)
    ftime=models.DateTimeField()


class PasswordProtectedUsers(models.Model):
    safebook = models.ForeignKey(flipping,on_delete = models.CASCADE)
    user = models.ForeignKey( User, on_delete= models.CASCADE )

class IPUsers(models.Model):
    safebook = models.ForeignKey(flipping,on_delete = models.CASCADE)
    IP = models.TextField(default='')
    # ipdate=models.DateTimeField()

class flipcustomize(models.Model):
    fobj=models.ForeignKey(flipping,on_delete=models.CASCADE)
    fskin=models.CharField(max_length=10,default="#50d8d7")
    flogo= models.ImageField(blank=True,  null=True ,upload_to = 'flip_logo')
    fbg=models.ImageField(blank=True,  null=True ,upload_to = 'flip_bg')
    fcpanel=models.CharField(max_length=10, default="#50d8d7")
    fcbg=models.CharField(max_length=10,default="#50d8d7")
    fclink=models.CharField(max_length=10,default="#50d8d7")
    ffavicon=models.ImageField(blank=True,  null=True ,upload_to = 'flip_favicon')
    fweb=models.URLField(max_length=100, default="https://aim2crack.in/")

class flipviews(models.Model):
    fobj=models.ForeignKey(flipping,on_delete=models.CASCADE)
    fdate=models.DateTimeField()
