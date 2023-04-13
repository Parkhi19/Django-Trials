from django.contrib.auth.models import User
from django.db import models
from users.models import Profile
from createquiz.models import createlink
from django.urls import reverse

class st_data(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.ForeignKey(createlink,on_delete=models.CASCADE)
    questions = models.TextField()
    answer = models.TextField()
    level = models.TextField()
    # def get_absolute_url(self):
    #     return reverse('result')

class result(models.Model):
    stans_id = models.ForeignKey(st_data,on_delete=models.CASCADE) 
    scores = models.TextField()
    def get_absolute_url(self):
        return reverse('exam-home')
    
class feedbackQue(models.Model):
    type_que = models.CharField(max_length=10)
    question = models.TextField()
    options = models.TextField()
    link = models.ForeignKey(createlink,on_delete=models.CASCADE)

class feedbackAnswers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.ForeignKey(createlink,on_delete=models.CASCADE)
    questions = models.TextField()
    answers = models.TextField()

class instructions(models.Model):
    link = models.ForeignKey(createlink,on_delete=models.CASCADE)
    instructions = models.TextField()

class errors(models.Model):
    page =  models.TextField()
    head =  models.TextField()
    text =  models.TextField()
