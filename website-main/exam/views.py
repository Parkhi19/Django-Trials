from django.forms.models import construct_instance
from django.http.response import HttpResponse
from quiz.models import questiondata
from createquiz.models import createlink,contacts,join
from django.shortcuts import redirect, render
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import talks,announce,Puzzle
from django.views.generic import (CreateView)
from django.contrib import messages
from users.models import Profile
from student.models import st_data,result
from users.views import isEmailVerified as ev

# Create your views here.
def home(request): 
        identity = ""
        pr = -1
        try:
            if request.user.last_login == None:
                x = 'y'
            else:
                x = 'n'
            t=Profile.objects.filter(user=request.user).first()
            identity = t.type
            pr = t.id
        except:
            x = 'y'
            identity = "n"
            pr = -1 
        talk = talks.objects.order_by('id').all().reverse()
        embed_link = ""
        for each in talk:
            if each.embed == None or each.embed == "":
                continue
            embed_link = each.embed
            break
        return render(request,"exam/Home.html",{"id":identity,"pr":pr,"check":x,"embed_link":embed_link})

@login_required
def yourquizzes(request):
    if not ev(request):
        return redirect('email-verify')
    a = []
    p = []
    t=Profile.objects.filter(user=request.user).first()
    if t.type == "s":
        questions_from_db = st_data.objects.filter(username_id = request.user.id).all()
        for i in questions_from_db:
            num = 0
            y = createlink.objects.filter(id = i.link_id).first()
            try:
                result_get = result.objects.filter(stans_id_id = i.id).first().scores
            except:
                continue
            tot = 0
            for marks in result_get.split(','):
                tot += int(marks)
                num+=1
            dic =   { 'link':y.link,
                        'creator':y.creator.username,
                        'topic_name':y.topic_name,
                        'course_name':y.course_name,
                        'maxima': y.maxima,
                        'minima': y.minima,
                        'mean': round(y.mean,3),
                        'marks':tot,
                        'total':num,
                    }
            if y.qtype == 'p':
                p.append({"det":dic,"ran":random.randint(1,12)})
            if y.qtype == 's':
                a.append({"det":dic,"ran":random.randint(1,12)})
        return render(request,'exam/student.html',{"Simple":reversed(a),"placement":reversed(p)})
    elif t.type == "t":
        quizzes = createlink.objects.filter(creator = request.user).all()
        simple = []
        done = []
        placement = []
        a,b = 0,0
        c = 10
        for i in quizzes:
            if i.link in done:
                continue
            if i.qtype == "s":
                simple.append(i)
                a+=1
            else:
                print(i.course_name)
                placement.append(i)
                b+=1
            done.append(i.link)
        return render(request,'exam/teacher.html',{'profile_id':t.id,'simple': reversed(simple),'placement': reversed(placement) })
    else:
        return redirect('../profile/'+str(t.id))


def about(request):
    return render(request,'exam/about.html')

def team(request):
    return render(request,'exam/team.html')

def contact(request):
    return render(request,'exam/contact.html')

def resource(request):
    return render(request,'exam/resource.html')

def placement_quizzes(request):
    return render(request,"exam/placment.html")

def contact_save(request):
    if request.method == 'POST':
        contact = contacts()
        contact.name  = request.POST["name"] 
        contact.phone  = request.POST["phone"] 
        contact.email  = request.POST["email"] 
        contact.Subject  = request.POST["Subject"] 
        contact.msg  = request.POST["msg"]
        if contact.name == '' or contact.phone == '' or contact.email == '' or contact.Subject == '' or contact.msg == '':
            messages.error(request,'Enter all the required inputs to send message.')
            return redirect('contact')
        contact.save() 
    messages.success(request,' "Thank you for connecting with us! We will get back to you soon". ')
    return redirect("contact")


def join_save(request):
    if request.method == 'POST':
        contact = join()
        contact.name  = request.POST["name"] 
        contact.phone  = request.POST["phone"] 
        contact.email  = request.POST["email"] 
        contact.Interests  = request.POST["Interests"] 
        contact.Why  = request.POST["Why"]
        print(list(request.POST.items()))
        if contact.name == '' or contact.phone == '' or contact.email == '' or contact.Interests == '' or contact.Why == '':
            messages.error(request,'Enter all the required inputs to send message.')
            return redirect('contact')
        contact.save() 
    messages.success(request,' "Thank you for your interest in joining us! We will get back to you soon".')
    return redirect("contact")

def add_it(request):
    if request.method == "POST":
        talk = talks()
        talk.name = request.POST["name"]
        talk.title = request.POST["title"]
        talk.time = request.POST["time"]
        talk.ytlink = request.POST["ytlink"]
        talk.placed = request.FILES["placed"]
        talk.dp = request.FILES["dp"]
        talk.fb = request.POST["fb"]
        talk.insta = request.POST["insta"]
        talk.github = request.POST["github"]
        talk.linkedin = request.POST["linkedin"]
        talk.tweeter = request.POST["tweeter"]
        talk.embed = request.POST["embed"]
        talk.save()
        return redirect("placement-talks")
    # return redirect("")

def edit_it(request):
    if request.method== "POST":
        # print(request.POST["id"],type(request.POST["id"]))
        talk = talks.objects.filter(id = request.POST["id"]).first()
        talk.name = request.POST["name"]
        talk.title = request.POST["title"]
        talk.time = request.POST["time"]
        talk.fb = request.POST["fb"]
        talk.insta = request.POST["insta"]
        talk.github = request.POST["github"]
        talk.linkedin = request.POST["linkedin"]
        talk.tweeter = request.POST["tweeter"]
        talk.ytlink = request.POST["ytlink"]
        talk.embed = request.POST["embed"]
        talk.save()
        return redirect("placement-talks")

def delete_it(request):
    if request.method == "POST":
        talks.objects.filter(id = request.POST["id"]).first().delete()
        return redirect("placement-talks")


def announce_edit(request):
    if request.user.is_staff or request.user.is_superuser:
        return  render(request,"announce/edit.html",{"tab":announce.objects.all().reverse()})
    return render(request,"student/error_404.html")
def announce_add(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request,"student/error_404.html")
    if request.method == "POST":
        ann = announce()
        ann.editor = request.user.username
        ann.date = request.POST["date"]
        ann.month = request.POST["month"]
        ann.title = request.POST["title"]
        ann.info = request.POST["info"]
        ann.link = request.POST["link"]
        ann.save()
        return redirect("edit-announce")

def announce_change(request,that):
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request,"student/error_404.html")
    ann = announce.objects.filter(id = that).first()
    if request.method == "POST":
        ann.editor = request.user.username
        ann.date = request.POST["date"]
        ann.month = request.POST["month"]
        ann.title = request.POST["title"]
        ann.info = request.POST["info"]
        ann.link = request.POST["link"]
        ann.save()
        return redirect("edit-announce")
    return render(request,"announce/change.html",{"give":ann})

def announce_del(request,that):
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request,"student/error_404.html")
    if request.method == "POST":
        announce.objects.filter(id=that).first().delete()
        return redirect("edit-announce")



def puzzle(request):
    puzzles = Puzzle.objects.all()
    puzzle = []
    hr = []
    for i in puzzles:
        x = i.like_user.split('+')
        if i.kind=='p':
            temp = False
            if str(request.user.id) in x:
                temp=True
            puzzle.append({'pzl':i.que ,"liked": temp,'a':i.ans , "pic" : str(i.img),'i':i.id,'l':i.logo,'s':i.soln })
    return render(request,'exam/puzzle.html',{'puzzles':puzzle})

def hr(request):
    puzzles = Puzzle.objects.all()
    hr = []
    for i in puzzles:
        if i.kind=='h':
            hr.append({'pzl':i.que ,'a':i.ans , "pic" : i.img ,'i':i.id})
    return render(request,'exam/hr.html',{'hrq':hr})
  
def likes(request,pk):
    if request.method == 'POST':
        it = Puzzle.objects.filter(id = pk).first()
        x = it.like_user.split('+')
        if str(request.user.id) in x:
            it.like-=1
            st = ""
            for each in x:
                if(each == str(request.user.id)): continue
                st+= str(each)+"+"
            it.like_user = st[:len(st)-1]
        else:
            it.like+= 1
            if it.like_user.strip() == "" or it.like_user == None:
                it.like_user = str(request.user.id)
            else:
                it.like_user += "+" +str(request.user.id)
        it.save()
    return HttpResponse("")



@login_required
def addpuzzle(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request,"public/something.html",{"msg":"You are not allowed to this page"})
    if request.method =='POST':
        p=Puzzle()
        p.que = request.POST["que"]
        try:
            p.img = request.FILES["img"]
        except:
            c=0
        try:
            p.logo = request.FILES["logo"]
        except:
            c=0
        p.soln=request.POST["soln"]
        p.ans = request.POST["ans"]
        p.kind = request.POST["kind"]
        p.like_user = ''
        p.dislike_user = ''

        if p.que == '' or p.ans == '' or p.kind == '' or p.soln=='':
            messages.error(request,'Fill the mandatory details to save')
            return redirect('addpuzzle')
        p.save()
        if p.kind == 'p':
            return redirect('puzzle')
        else:
            return redirect('hr')
    return render(request,"exam/addpuzzle.html")

