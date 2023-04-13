from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll_no=models.TextField()
    college=models.TextField()
    avatar = models.CharField(max_length=2)
    type=models.CharField(max_length=15)
    def __str__(self):
        return f'{self.user.username} Profile'
        
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('createquiz-home')


 
class otp(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    email = models.EmailField()
    time = models.DateTimeField()
    

# Create your models here.

class branding(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    blogo= models.ImageField(blank=True,  null=True ,upload_to = 'brand_logo')
    bname=models.CharField(max_length=10,default="Aim2crack")    
    bweb=models.URLField(max_length=100, default="https://aim2crack.in/")
    bfavicon=models.ImageField(blank=True,  null=True ,upload_to = 'brand_favicon')


