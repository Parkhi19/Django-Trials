from django.db import models
from django.urls import reverse

class CreateLink(models.Model):

    # dummy fields
    link=models.CharField(max_length=12)
    no_of_submissions= models.IntegerField(blank=False, null=True)


    # method returning URL
    def get_absolute_url(self):
        return reverse('tutorials-home')
