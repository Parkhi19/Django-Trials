from django.db import models

# Create your models here.
class talks(models.Model):
    name = models.CharField(max_length=50)
    title = models.TextField()
    time = models.TextField()
    placed = models.ImageField(blank=True,  null=True ,upload_to = 'talks')
    dp = models.ImageField(blank=True,  null=True ,upload_to = 'talks')
    fb = models.TextField()
    insta = models.TextField()
    github = models.TextField()
    linkedin = models.TextField()
    tweeter = models.TextField()
    ytlink = models.TextField()
    embed = models.TextField()

class announce(models.Model):
    date = models.IntegerField()
    month = models.CharField(max_length=5)
    title = models.TextField()
    info = models.TextField()
    link = models.TextField()
    editor = models.CharField(max_length=50)

    
    
class Puzzle(models.Model):
    que=models.TextField()
    img=models.ImageField(blank=True,  null=True ,upload_to = 'puzzle_img')
    ans=models.TextField()
    kind=models.CharField(max_length=10)
    like=models.IntegerField(default=0)
    soln=models.TextField()
    logo=models.ImageField()
    dislike=models.IntegerField(default=0)
    like_user=models.TextField()
    dislike_user=models.TextField()
