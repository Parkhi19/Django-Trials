from django.db import models
import random
from django.contrib.auth.models import User
from django.db.models.fields import CharField, EmailField, TextField
from django.urls import reverse
from users.models import Profile
#from quiz.models import questiondata
# Create your models here.
    
class createlink(models.Model):
    link=models.CharField(max_length=12)
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=50)
    course_name = models.CharField(max_length=50)
    start = models.DateTimeField()
    margin = models.DateTimeField()
    qtype = models.CharField(max_length=5)
    result_time = models.DateTimeField()
    minima = models.TextField(blank=True,  null=True)
    maxima = models.TextField(blank=True,  null=True)
    mean = models.FloatField(default=0) 
    ttime = models.CharField(null=True,blank=True,max_length=10)
    ttype = models.CharField(null=True,blank=True,max_length=5)
    responses = models.TextField(blank=True, null=True)
    t_responses = models.IntegerField(default=0)
    t = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('quiz-home')

class feedback(models.Model):
    star1 = models.CharField(max_length=2)
    star2 = models.CharField(max_length=2)
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.ForeignKey(createlink,on_delete=models.CASCADE)
    ans = models.TextField()
    cheat = models.TextField()
    prevent = models.TextField()
    rating = models.IntegerField()

    def get_absolute_url(self):
        return reverse('exam-home')

class contacts(models.Model):
    name = CharField(max_length=60)
    phone = CharField(max_length= 18)
    email = EmailField()
    Subject = CharField(max_length=50)
    msg = TextField()
    def get_absolute_url(self):
        return reverse('contact')

class join(models.Model):
    name = CharField(max_length=60)
    phone = CharField(max_length= 18)
    email = EmailField()
    Interests = CharField(max_length=30)
    Why = TextField()
    def get_absolute_url(self):
        return reverse('contact')