from users.models import Profile
from CreateAssignment.models import CreateLink 
from CreateAssignment.models import StudentScore

from django.shortcuts import render
import random
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def randnumber(a,b):
    return random.randint(a,b)

@login_required
def asummary(request):
    pro=Profile.objects.filter(user=request.user).first()
    if pro.type=='t':
        codes=CreateLink.objects.filter(creator=request.user).all()
        return render(request, "CreateAssignment/safebook.html", {"simple": codes})
    elif pro.type=='s':
        codes=StudentScore.objects.filter(user=request.user).all()
        return render(request, "student_assignment/safebook_stu.html", {"simple": codes})
    else:
        return JsonResponse({"status":"Yet to be worked on..."})