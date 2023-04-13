from datetime import datetime
from xml.dom.minidom import Document
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import certies
import datetime
import random
from django.contrib.auth.decorators import login_required


def codeGenerator(request):
    a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    str = ""
    for i in range(16):
        it = random.randint(0,len(a))
        str += a[it]
    return str

@login_required
def add_certi(request):
    if not request.user.is_superuser:
        return HttpResponse(status = 403)
    if request.method =='POST':
        it= certies()
        it.code= codeGenerator(request)
        it.date_issued = datetime.datetime.now().strftime("%Y-%m-%d")
        it.name =request.POST["name"]
        it.email = request.POST["email"]
        it.date_joined = request.POST["date_joined"]
        it.date_left = request.POST["date_left"]
        it.team_worked= request.POST["team"]
        it.save()
        return redirect('all-certi')
    return render(request,'certies/add_certi.html')

def email_send(request,code):
    if not request.user.is_superuser:
        return HttpResponse(status = 403)
    doc = certies.objects.filter(code = code).first()
    return render(request,'certies/email_send.html')


def send_it(request):
    return

def all_certi(request):
    if not request.user.is_superuser:
        return HttpResponse(status = 403)
    certificates = certies.objects.all()
    return render(request,'certies/all_certi.html',{"certies":certificates})

def verify_certi(request,code):
    doc = certies.objects.filter(code = code).first()
    return render(request,"certies/verify_certi.html",{"it":doc})
