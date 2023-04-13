from django.contrib import messages
from CreateAssignment.models import CreateLink
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .profile_check import ProfileCheck



@login_required
def LinkDelete(request,link):
   chk=ProfileCheck(request,link)
   if chk==1 and request.method == "POST" :
      x = CreateLink.objects.filter(link = link).all().delete()
      messages.success(request,"Assignment has been deleted successfully")
      return redirect('../../') 
   # elif chk ==0:
   #    return render(request,'CreateAssignment/something.html',{'msg':"You are not allowed on this page. Please go back."})
   return render(request,"CreateAssignment/deletelink.html")
