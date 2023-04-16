from os import link
from django.contrib import admin
from django.urls import path
 
from .views import *

urlpatterns = [

    path('',LinkCreate,name='Summary-Assignment'),     
  
]