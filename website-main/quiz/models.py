from django.db import models
from django.urls import reverse
from createquiz.models import createlink

# Create your models here.
class questiondata(models.Model):
    type = models.CharField(max_length=5)
    level = models.CharField(max_length=5)
    time = models.IntegerField()
    question = models.TextField()
    options = models.TextField()
    photo = models.ImageField(blank=True,  null=True ,upload_to = 'ques_img')
    correct = models.TextField()
    explanation = models.TextField()
    link=models.ForeignKey(createlink,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('quiz-home')