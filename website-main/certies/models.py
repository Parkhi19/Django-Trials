from django.db import models

# Create your models here.
class certies(models.Model):
    name = models.TextField()
    code = models.CharField(max_length=16)
    date_joined = models.DateField()
    date_left = models.DateField()
    team_worked = models.TextField()
    date_issued = models.DateField()
    email = models.EmailField()
    isMale = models.BooleanField(default=True)
    
