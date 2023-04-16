import datetime 
from django.contrib import messages
from users.models import Profile
from tutorials.models import CreateLink
from django.shortcuts import redirect, render
import random

from django.contrib.auth.decorators import login_required
from django.contrib import messages

def randlink():
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    letters = []
    for i in alphabets:
        letters.append(i)
    link ='' 
    for i in range(10):
        link += letters[random.randint(0,25)]
        if i==2 or i == 6 :
            link+='-'
    return link


@login_required
def LinkCreate(request):
  
        if request.method == "POST":
           


            create = CreateLink()
            create.no_of_submissions = request.POST["no_of_submissions"]

            # create.course_name = request.POST["course_name"].strip().replace(" ","-")
            # create.assignment_name = request.POST["assignment_name"].strip().replace(" ","-")
            # create.start = request.POST["start"]
            # create.first_sub_time = request.POST["first_sub_time"]
            # create.extend = request.POST["extend"]
            # create.second_sub_time = None if request.POST["second_sub_time"] == "" else request.POST["second_sub_time"]
            # create.no_of_submissions = request.POST["no_of_submissions"]
            # create.perc_penalty = None if request.POST["perc_penalty"] == "" else request.POST["perc_penalty"]
            # create.notif = request.POST["notif"]  
            # create.face_rec = request.POST["face_rec"] 
            # create.neg_mark = request.POST["neg_mark"]
            # create.res_anno= request.POST["res_anno"]
            # create.creator_id = request.user.id
            # create.result_time = None if request.POST["result_time"] == "" else request.POST["result_time"]
            link = None
            while(True):
                link = randlink()
                if CreateLink.objects.filter(link= link).first() is None:
                    break
            create.link= link
            create.save()
            # Instruction.objects.create(instructions= "", assignment_id = create.id )
            messages.success(request,f"Assignment has been created successfully!")
            return redirect("../"+link+"/")
        return render(request,"home.html")


