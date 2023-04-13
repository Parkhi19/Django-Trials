from django.contrib import auth
from django.http.response import HttpResponse
from users.models import Profile,otp
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,UserDetailForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import branding
# from student.views import topThree
import random
import datetime
import pytz
import os
import json
from django.conf import settings





def isEmailVerified(request):
    if EmailAddress.objects.filter(user = request.user).first() == None or EmailAddress.objects.filter(user = request.user).first().verified == 0:
        return False
    return True


# Create your views here.
def register(request):
    if request.method == 'POST' :
        register = User()
        if request.POST["college"] == '' or request.POST["roll_no"] == '' or  request.POST["username"]=="" or request.POST["password1"] == ""  or request.POST["password2"]=="":
            messages.error(request,'Please fill all the informations!')
            return redirect('register')
        if User.objects.filter(email=request.POST["email"].lower()).first() is not None:
            messages.error(request,'A user with that email already exist!')
            return redirect('register')
        if User.objects.filter(username=request.POST["username"].lower()).first() is not None:
            messages.error(request,'That username already exist!')
            return redirect('register')
        if request.POST["password1"] != request.POST["password2"] and len(request.Post["password1"]) < 8 :
            messages.error(request,'Either the passwords you have entered are not same or the length of passwords is less than 8!')
            return redirect('register')
        register.username = request.POST["username"].lower()
        register.email = request.POST["email"].lower()
        register.set_password(request.POST["password1"])
        register.save()
        y = User.objects.filter(username = request.POST["username"].lower()).first().id
        pro = Profile.objects.filter(user_id = y).first()
        pro.college = request.POST["college"]
        pro.roll_no = request.POST["roll_no"]
        if request.POST["role"] == "s": 
            pro.type = 's'
        elif request.POST["role"] == "t":
            pro.type = "t"
        else:
            messages.error(request,"Select the correct role...")
            return redirect('./')
        pro.avatar = '1'
        pro.save()
        
        messages.success(request,"Logged In successfully as "+request.POST["username"].lower())
        user = authenticate(request, username = request.POST["username"].lower(), password = request.POST["password1"])
        branding.objects.create(user=request.user)
        login(request,user)
        return redirect('email-verify')
    else:
        form =UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile_edit(request,pk):
    if not isEmailVerified(request):
        return redirect('email-verify')
    if pk != request.user.profile.id:
        return redirect("https://aim2crack.in/profile/"+str(request.user.profile.id))
    pro = Profile.objects.filter(user_id = request.user.id).first()     
    if request.method == 'POST':
        if request.POST["roll_no"] == "" and pro.type == "s":
            messages.error(request,"None of the following fields can be empty.")
            return redirect("./")
        if request.POST["college"] == "" or request.POST["avatar"] == "":
            messages.error(request,"None of the following fields can be empty.")
            return redirect("./")
        user = request.user
        user.first_name = request.POST["first"].upper()
        user.last_name = request.POST["last"].upper()
        user.save()
        pro.roll_no = request.POST["roll_no"]
        pro.college = request.POST["college"]
        pro.avatar = request.POST["avatar"]
        pro.save()
        messages.success(request,"Your details saved successfully")
        return redirect("./")
    return render(request,"users/profile.html",{"profile":pro})
        
        
        


def do_login(request):
    username = ''
    if request.method == 'POST':
        username = request.POST['email'].lower()
        password = request.POST['password']
        try:
            users = User.objects.filter(email=username).first().username
        except:
            users = username
        user = authenticate(request, username=users, password=password)
        if user is not None:
            login(request,user)
            try:
                if request.POST["next"]:
                    return redirect('./../../..'+request.POST["next"])
            except:
                return redirect('exam-home')
        else:
            messages.error(request,'Email or Password you have entered is wrong.')
    return render(request,'users/login.html',{"email":username})


@login_required
def change_password(request):
    if request.method == 'POST':
        old = request.POST['password']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        user = authenticate(request, username = request.user, password = old)
        if user is not None:
            if pass1 != pass2:
                messages.error(request,'New passwords you have entered are not matching.')
                return redirect('change-password')
            u = User.objects.get(username = user)
            u.set_password(pass1)
            u.save()
            messages.success(request,"Password changed successfully to \""+pass1[:1]+'*'*(len(pass1)-2)+pass1[len(pass1)-1:]+'\"')
            user = authenticate(request,username = request.user,password = pass1)
            login(request,user)
            return redirect('../profile/'+str(int(request.user.id)-4))
        else:
            messages.error(request,'Old Password you have entered is not correct.')
    return render(request,'users/change_password.html')




def getotp():
    s = ""
    for i in range(6):
        s = s+str(random.randint(0,9))
    return s

@login_required
def emailVerify(request):
    checkit= EmailAddress.objects.filter(user = request.user).first()
    if checkit is not None and checkit.verified == 1:
        return render(request,"public/something.html",{"msg":"Your Email is already verified."})
    it =otp.objects.filter(user = request.user).first()
    IST = pytz.timezone('Asia/Kolkata')
    if it == None :
        real = getotp()
        it = otp()
        it.code = real
        it.email = request.user.email
        it.time = datetime.datetime.now(IST)  
        it.user = request.user
        it.save()
        send_mail(
            'OTP for Email Verification at Aim2Crack.',
            'This is your OTP for email verification '+real+'. Do not share it with anyone.',
            'Aim2Crack',
            [request.user.email],
            fail_silently=False,
        )
    else:
        a= it.time
        b = datetime.datetime.now(IST)
        c = b-a
        x = divmod(c.seconds,60)
        if x[0]>15:
            real = getotp()
            it.code = real
            it.email = request.user.email
            it.time = datetime.datetime.now(IST)  
            it.user = request.user
            it.save()
            send_mail(
                'OTP for Email Verification at Aim2Crack.',
                'This is your OTP for email verification '+real+'. Do not share it with anyone.',
                'Aim2Crack',
                [request.user.email],
                fail_silently=False,
            )
    if request.method == "POST":
        a= it.time
        b = datetime.datetime.now(IST)
        c = b-a
        x = divmod(c.seconds,60)
        if  x[0] > 15:
            return render(request,"OTP EXPIRED, new OTP sent to your email")
        if it.code == str(request.POST["otp"]):
            messages.success(request,'Email Verified')
            it = EmailAddress.objects.filter(user = request.user).first()
            if it == None:
                it = EmailAddress()
            it.verified = 1
            it.primary = 1
            it.user = request.user
            it.email = request.user.email
            it.save()
            return redirect('../profile/'+str(request.user.id))
        else:
            messages.error(request,'OTP didn\'t match Try again')
    return render(request,"email_verify/main.html")

@login_required
def send(request):
    if request.method == "POST":
        it =otp.objects.filter(user_id = int(request.POST["user"])).first()
        IST = pytz.timezone('Asia/Kolkata')
        a= it.time
        b = datetime.datetime.now(IST)
        c = b-a
        x = divmod(c.seconds,60)
        if x[0] <1:
            return HttpResponse('You have to wait for one minute before resending code')    
        elif x[0] <=15:
            it.time = datetime.datetime.now(IST)  
            it.save()
            send_mail(
            'OTP for Email Verification at Aim2Crack.',
            'This is your OTP for email verification '+it.code+'. Do not share it with anyone.',
            'Aim2Crack',
            [request.user.email],
            fail_silently=False,
            )
        return HttpResponse('Email has been resent successfully if you still have not found it check in spam folder in you inbox')
    return HttpResponse('Encountered some problem')


def do_lower(request):
    A = []
    B = set()
    X = User.objects.all()
    for each in X:
        if each.username.lower not in B:
            try:
                each.username = each.username.lower()
                each.email = each.email.lower()
                B.add(each.username.lower())
                each.save()
            except:
                A.append(each.username)
        else:
            A.append(each.username)
            continue
    return render(request,"users/it.html",{"msg":"Everything done Manish","yes":B,"no":A})

# @login_required
# def brands(request):
#     t=Profile.objects.filter(user=request.user).first()
#     if t.type == "s":
#          return render(request,"flipping/something.html",{"msg":"Only faculty can avail branding services"})
#     else:
#         brand= branding.objects.filter(user = request.user).first()
#         if brand == None:
#              branding.objects.create(user=request.user)
#         if request.method == 'POST' :

#             if 'blogo' in request.FILES:
#                 try:
#                     os.remove(os.path.join(settings.MEDIA_ROOT,str(brand.blogo)))
#                 except:
#                     pass
#                 brand.blogo = request.FILES["blogo"]

#             if 'bfavicon' in request.FILES:
#                 try:
#                     os.remove(os.path.join(settings.MEDIA_ROOT,str(brand.bfavicon)))
#                 except:
#                     pass
#                 brand.bfavicon = request.FILES["bfavicon"]
#             brand.bname=request.POST["bname"]
#             brand.bweb=request.POST["bweb"]
#             brand.save()
#             messages.success(request,"Settings updated")
#             # return redirect('../')
#         return render(request,'branding/branding.html',{"brand":brand})

        
# def delete_brand(request):
#     if request.method == 'POST':
#         what = int(request.POST["what"])
#         ques = branding.objects.filter(user = request.user).first()
#         if what == 1:
#             #delete logo
#             # print(ques.flogo)
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.blogo)))
#                 ques.blogo = None
#             except:
#                 print('flogo not here')
#                 ques.blogo = None
#             ques.save()
#             return HttpResponse(json.dumps({"status": "Blogo Deleted"}))
#         if what == 2:
#             #delete favicon
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.bfavicon)))
#                 ques.bfavicon =  None
#             except:
#                 print('favicon not here')
#                 ques.bfavicon = None
#             ques.save()
#         return HttpResponse(json.dumps({"status": "Favicon Deleted"}))
#     return HttpResponse({})
