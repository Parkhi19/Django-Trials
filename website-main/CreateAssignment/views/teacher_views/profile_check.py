from users.models import Profile
from CreateAssignment.models import CreateLink
from django.shortcuts import render
import random
from django.contrib.auth.decorators import login_required
import datetime 
from django.contrib import messages
from CreateAssignment.models import CreateLink
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse


@login_required
def ProfileCheck(request,link):
    pro=Profile.objects.filter(user=request.user).first()
    link=CreateLink.objects.filter(link=link).first()
    print(pro.user.id)
    print(link.creator_id)
    if pro.type=='s':
        return 0
        # return render(request,'CreateAssignment/something.html',{'msg':"Student profile is not permitted for this action"})
    if pro.user.id != link.creator_id:
        # return render(request,'CreateAssignment/something.html',{'msg':"You are not allowed on this page. Please go back."})
        # return HttpResponse("Your Profile is not allowed for this operation")
        return 0
    # return render(request,'CreateAssignment/something.html',{'msg':"You are not allowed on this page. Please go back."})
    return 1
