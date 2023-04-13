import createquiz
import datetime
from django.contrib import messages
from createquiz.models import createlink
from django.shortcuts import redirect, render
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,DeleteView
from django.contrib import messages
from exam.models import talks as discussion
from users.models import Profile
from student.models import st_data,result
from student.views import topThree
from users.views import isEmailVerified as ev

RANDOM_LINK_GENERATED=''
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
# Create your views here.
@login_required
def linkcreate(request):
    if not ev(request):
        return redirect('email-verify')
    if request.user.profile.type == "s":
        return render(request,"public/something.html",{"msg":"Student profile is not permitted to create quiz. You can avail other services","videos":topThree()})
    if request.method == "POST":
        try:
            if request.POST["course_name"].strip() == "" or request.POST["topic_name"].strip() == "" or request.POST["result"] == "" or request.POST["start"] =="" or request.POST["ttype"] =="" or request.POST["margin"] =="":
                messages.error(request,"Fill all the details to continue!")
                return redirect("./")
        except:
                messages.error(request,"Fill all the details to continue!")
                return redirect("./")
        start = request.POST["start"].replace('T',' ')
        margin = request.POST["margin"].replace('T',' ')
        result = request.POST["result"].replace('T',' ')
        ajf =str(datetime.datetime.strptime(margin, '%Y-%m-%d %H:%M')-datetime.datetime.strptime(start, '%Y-%m-%d %H:%M'))
        if ajf[0] == '-' or ajf == '0:00:00':
            messages.error(request,'Last Login time can not be same or greater than the quiz start time')
            return redirect('./')
        if str(datetime.datetime.strptime(result, '%Y-%m-%d %H:%M')-datetime.datetime.strptime(margin, '%Y-%m-%d %H:%M'))[0] == '-':
            messages.error(request,'Result Opening time can not be greater than the Last Login time')
            return redirect('./')
        create = createlink()
        create.course_name = request.POST["course_name"].strip().replace(" ","-")
        create.topic_name = request.POST["topic_name"].strip().replace(" ","-")
        create.start = request.POST["start"]
        create.margin = request.POST["margin"]
        create.qtype = request.POST["qtype"]
        create.creator_id = request.user.id
        create.ttype = request.POST["ttype"]
        create.ttime = "00:30:00"
        create.result_time = request.POST["result"]
        link = None
        while(True):
            link = randlink()
            if createlink.objects.filter(link= link).first() is None:
                break
        create.link= link
        create.save()
        messages.success(request,"Quiz has been created successfully!")
        return redirect("../"+link+"/")
    return render(request,"exam/Creating.html")


@login_required
def deletelink(request,link):
    if not ev(request):
        return redirect('email-verify')
    if request.user.profile.type == "s":
        return render(request,"public/something.html",{"msg":"You are not allowed to delete this quiz!","videos":topThree()})
    if request.method == "POST":
        x = createlink.objects.filter(link = link).all().delete()
        return redirect('quizzes')
    return render(request,"createquiz/deletelink.html")

@login_required
def deletesection(request,link):
    if not ev(request):
        return redirect('email-verify')
    if request.user.profile.type == "s":
        return render(request,"public/something.html",{"msg":"You are not allowed to delete this quiz section!","videos":topThree()})
    x = createlink.objects.filter(link = link).all()
    some = []
    for i in x:
        some.append(i.topic_name)
    if request.method == "POST":
        createlink.objects.filter(link = link).filter(topic_name = list(request.POST.items())[1][1]).delete()
        if len(some) == 1:
            return redirect('quizzes')
        return redirect('../.')
    return render(request,"createquiz/delete-section.html",{"all":some})

def talks(request):
    m = ""
    try:
        m = str(int(request.user.id)-4)
    except:
        m = "0"
    top = []
    rem = []
    ct = 0
    for each in reversed(discussion.objects.reverse().all()):
        if ct<5:
            top.append(each)
            ct+=1
        else:
            rem.append(each)
    allowed = [15]
    return render(request,"createquiz/talks.html",{"pr":m ,"top":top,"rem":rem,"allowed":allowed})



def stdata_tab(request):
    context = st_data.objects.all()
    resultdata = result.objects.all()
    return render(request,"createquiz/stdata.html",{"stdata":context,"res":resultdata})
