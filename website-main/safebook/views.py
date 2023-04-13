from http.client import HTTPResponse
from django.shortcuts import render
from datetime import datetime 
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse
import random
from django.contrib import messages
from .models import *
import os
from users.models import Profile
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
import socket   
from users.models import branding
import pytz

from django.core import serializers


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

# def pagecount():
#     file = open('./../../media/flipupload/202111011104.pdf', 'rb')
#     readpdf = PyPDF2.PdfFileReader(file)
#     a = readpdf.numPages
#     print(a)
#     return a

  

@login_required
def flip_upload(request):
    brand=branding.objects.filter(user=request.user).first()
    # print(brand.bfavicon)
    create=None
    if request.method == 'POST':
        create=flipping()
        create.creator_id = int(request.user.id)
        link = randlink()
        create.link= link
        create.fname = request.POST["fname"]
        create.upload=request.FILES["fileu"]
        create.fsub=request.POST["fsub"]
        create.ftime=datetime.now()
        create.dtime=   None if request.POST["dtime"] == "" else request.POST["dtime"]
        create.dates=[]
        create.save()
        flipprivacy.objects.create(link = create, fprivacy ='b' )
        flipcustomize.objects.create(fobj=create, flogo=brand.blogo, ffavicon=brand.bfavicon)
        messages.success(request,f"File has been uploaded successfully!")
        return redirect('flipsummary')    

    return render(request,'flipping/flip.html',{"detail":create, "userr":brand})

@login_required
def yourflips(request):
    t=Profile.objects.filter(user=request.user).first()
    # print(request.user.branding.blogo)
    # print(request.user.branding.blogo)
    if t.type == "s":
         return render(request,"flipping/something.html",{"msg":"You need a faculty profile to create safebooks!. You can avail other services"})
    elif t.type == "t":
        flips = flipping.objects.filter(creator = request.user).all()
        # pages=pagecount()
        # print(pages)
        simple = []
        for i in flips:
                simple.append(i)
                # print(i.link)
        return render(request,'flipping/flipview.html',{'simple': reversed(simple)})

@login_required
def deleteflip(request,link):
    if request.method == 'POST':
        doc=flipping.objects.filter(link = link).all()
        for document in doc:
            document.delete()
        messages.success(request,"Safebook deleted")
        return redirect('../../view')
    return render(request,'flipping/delete.html')

@login_required
def editflip(request,link):
    ques=flipping.objects.filter(link = link).first()
    # print(ques)
    start_v = str(ques.dtime)[:10]+'T'+str(ques.dtime)[11:16]
    if request.method == 'POST':
        if 'fileu' in request.FILES and ques.upload:
            os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.upload)))
            ques.upload=request.FILES["fileu"] 
        ques.fname = request.POST["fname"]
        ques.ftime=datetime.now()
        ques.dtime= None if request.POST["dtime"] == "" else request.POST["dtime"]
        ques.save()
        messages.success(request,"Safebook updated")
        return redirect('../../view')
    return render(request,'flipping/flip.html',{"quest":ques,"file":str(ques.upload)[11:], "endtime":start_v})


# @login_required
# def privacyflip(request,link):
#     quest=flipping.objects.filter(link=link).first()
    
#     ques = flipprivacy.objects.filter(link = quest).first()
#     if request.method == 'POST':
#         ques.link=quest
#         if ques.fprivacy == 'd' and request.POST["fprivacy"] != 'd':
#             deletepasswords(request,quest.id)
        
#         ques.fprivacy = request.POST["fprivacy"]
#         try:
#             ques.fdomain = request.POST["fdomain"]
#         except:
#             pass
#         try:
#             if ques.fpass != reqeust.POST["fpass"]:
#                 deletepasswords(request,quest.id)
#             ques.fpass = request.POST["fpass"] 
#         except:
#             pass
#         ques.save()
#         messages.success(request,"Privacy settings updated")
#         return redirect('../../view')
#     ques=flipprivacy.objects.filter(link=quest).first()
    
#     return render(request,'flipping/flipprivacy2.html',{"qp":ques,"var":ques.fprivacy})
# @login_required
# def addtocollections(request,link):
#     creator=request.user
#     if request.method == 'POST':
#         flip=flipping.objects.filter(link=link).first()
#         if not request.user.is_authenticated :
#             return HttpResponse(json.dumps({"msg":"login is required","status":False}))
#         if creator == flip.creator:
#             return HttpResponse(json.dumps({"msg":"your own safebook cant be added to collection","status":False}))
#         added = flipcollection.objects.filter(fobj = flip).filter(creator = request.user)
#         if added:
#             added.delete()
#             return HttpResponse(json.dumps({"msg":"Already added","status":False}))
#         else:
#             ques=flipcollection()
#             ques.creator=creator
#             ques.fobj = flip
#             ques.ftime =datetime.now()
#             ques.save()
#             return HttpResponse(json.dumps({"msg":"successfully added","status":True}))
#     return HttpResponse(json.dumps({"msg":"Failed","status":False}))


# def passcheck(request,link):
#     if request.method == 'POST':
#         hostname=socket.gethostname()   
#         IPAddr=socket.gethostbyname(hostname) 
#         if str(IPAddr) == '127.0.0.1':
#             return HttpResponse(json.dumps({"result":False,'msg':'you need to connect to internet'}))
#         safebook = flipping.objects.filter(link = link).first()
#         password = flipprivacy.objects.filter(link = safebook).first().fpass
#         if password == request.POST['password']:
#             if request.user.is_authenticated:
#                 PasswordProtectedUsers.objects.create(
#                     user = request.user,
#                     safebook = safebook
#                 )
#             else:        
#                 IPUsers.objects.create(
#                     IP = str(IPAddr),
#                     safebook = safebook
                    
#                 )
#             return HttpResponse(json.dumps({"result":True,'address':str(safebook.upload)}))
#         else:
#             return HttpResponse(json.dumps({"result":False}))

# @login_required
# def studentflip(request,link):
#     brand=branding.objects.filter(user=request.user).first()
#     flip=flipping.objects.filter(link=link).first()
#     privacy = flipprivacy.objects.filter(link = flip).first()
#     customf=flipcustomize.objects.filter(fobj=flip).first()
    
#     if flip == None:
#          return render(request,"flipping/something.html",{"msg":"This flipbook is not available! Contact owner if this is an mistake!"})
#     # if flip.dtime == None:
#     #     return render(request,'flipping/something.html',{"msg":"Some print"})
#     # start_d = str(flip.dtime).split('+')[0]
#     # if durations(start_d) == 1:
#     #      return render(request,"flipping/something.html",{"msg":"This flipbook is disabled ! Contact owner if this is an mistake!"})
#     if privacy.fprivacy == 'b' and not request.user.is_authenticated:
#         return redirect('../../../../login/?next=/f/'+link+'/sview/')
#     if privacy.fprivacy == 'c':
#         if request.user.is_authenticated:
#             return HttpResponse("you are not allowed to access this safebook. Login with your domain or contact the creator")
#         domain = request.user.email[request.user.email.find('@')+1:]
#         if domain != privacy.fdomain:
#             return HttpResponse("you are not allowed to access this safebook. Login with your domain or contact the creator")
#     rem = 'a'
#     if privacy.fprivacy == 'd':
#         if not request.user.is_authenticated:
#             hostname=socket.gethostname()   
#             IPAddr=socket.gethostbyname(hostname)  
#             if not IPUsers.objects.filter(IP = str(IPAddr)).filter(safebook = flip):
#                 rem = 'd'
#         if request.user.is_authenticated and not PasswordProtectedUsers.objects.filter(user = request.user).filter(safebook = flip):
#             rem ='d'
#     if privacy.fprivacy == 'e' and (not request.user.is_authenticated or request.user != flip.creator):
#         return redirect('The safebook is private. Only owner can access')
    
#     btn = "Add to Collection"
#     if request.user.is_authenticated:
#         ques = flipcollection.objects.filter(fobj = flip).filter(creator = request.user)
#         if ques:
#             btn = "Remove from Collection"
#             ques = ques.first()
#             ques.ftime =datetime.now()  
#             ques.save()

#     count=flip.times
#     countn=count+1
#     flip.times=countn
#     flip.save()
#     fvi=flipviews()
#     fvi.fobj=flip
#     fvi.fdate=datetime.now()
#     fvi.save()
#     nam=str('pdf')
#     return render(request,'flipping/web/viewer.html',{"qp":flip,'link':flip.link,"btn":btn,"pass": rem ,"address": str(flip.upload),"cf":customf, "userr":brand, "name":nam })


# @login_required
# def collectflip(request):
#     # if not ev(request):
#     #     return redirect('email-verify')
#         flips = flipcollection.objects.filter(creator = request.user).all()
#         simple = []
#         content={}
#         for i in flips:
#             content={}
#             fo=flipping.objects.filter(id=i.fobj_id).first()
#             content["fname"]=fo.fname
#             content["fsub"]=fo.fsub
#             content["ftime"]=i.ftime
#             content["flink"]=fo.link
#             content["fcreator"]=fo.creator
#             content["num"]=i.id
#             simple.append(content)
#         return render(request,'flipping/flipcollections.html',{'simple': reversed(simple) , "content":content})
# @login_required
# def removeflip(request,link):
#     if request.method == 'POST':
#         doc=flipcollection.objects.filter(link=link).all()
#         for document in doc:
#             document.delete()
#         return redirect('flipcollection')
#     return render(request,'CreateAssignment/delete.html')
# @login_required
# def shareflip(request,nu):
#     doc=flipping.objects.filter(link=link).first()
#     return render(request,'flipping/sharelink.html',{"do":doc})

# def delete_branding(request,link,nu):
#     if request.method == 'POST':
#         what = int(request.POST["what"])
#         ques = flipcustomize.objects.filter(fobj_id = nu).first()
#         print(nu)
#         if what == 1:
#             #delete logo
#             # print(ques.flogo)
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.flogo)))
#                 ques.flogo = None
#             except:
#                 print('flogo not here')
#                 ques.flogo = None
#             ques.save()
#             return HttpResponse(json.dumps({"status": "Flogo Deleted"}))
#         if what == 2:
#             #delete background picture
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.fbg)))
#                 ques.fbg =  None
#             except:
#                 print('fbg not here')
#                 ques.fbg = None
#             ques.save()
#             return HttpResponse(json.dumps({"status": "Background Deleted"}))
#         if what == 3:
#             #delete favicon
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.ffavicon)))
#                 ques.ffavicon =  None
#             except:
#                 print('favicon not here')
#                 ques.ffavicon = None
#             ques.save()
#         return HttpResponse(json.dumps({"status": "Favicon Deleted"}))
#     return HttpResponse({})




# @login_required
# def customflip(request,link):
#     quest=flipping.objects.filter(link=link).first()
#     ques=flipcustomize.objects.filter(fobj=quest).first()
#     brand=branding.objects.filter(user=request.user).first()
#     # ques=flipcustomize()
#     if request.method =='POST':
#         ques.fobj=quest
#         ques.fskin=request.POST["fskin"]
#         ques.fcpanel=request.POST["fcpanel"]
#         ques.fcbg=request.POST["fcbg"]
#         ques.fclink=request.POST["fclink"]
#         ques.fweb=request.POST["fweb"]
        
#         if 'flogo' in request.FILES:
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.flogo)))
#             except:
#                 pass
#         if 'fbg' in request.FILES:
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.fbg)))
#             except:
#                 pass
#         if 'ffavicon' in request.FILES:
#             try:
#                 os.remove(os.path.join(settings.MEDIA_ROOT,str(ques.ffavicon)))
#             except:
#                 pass
#         try:
#             ques.flogo=request.FILES["flogo"]
#         # print(ques.flogo)
#         except: 
#             pass

#         try:
#             ques.fbg=request.FILES["fbg"]
#         except: 
#             pass

#         try:
#             ques.ffavicon=request.FILES["ffavicon"]
#         except: 
#             pass

#         ques.save()
#         messages.success(request,"Settings updated")
     
#         return redirect('../../view')
#     ques=flipcustomize.objects.filter(fobj=quest).first()
#     # print(ques)
#     return render(request,'flipping/flipcustom.html',{"quest":ques,"id": quest.id, "brand":brand})
    

# def viewcounts(request,link):
#     quest=flipping.objects.filter(link=link).first()
#     fviews=flipviews.objects.filter(fobj=quest).all()
#     dtime = serializers.serialize("json", fviews)
#     if len(fviews)==0:
#         return render(request,"flipping/something.html",{"msg":"There are no views currently for this flipbook"})
#     return render(request,'flipping/flipcount.html',{"datearray":dtime,"dates":fviews})

# def deletepasswords(request,nu):
#     # chk=PasswordProtectedUsers.objects.filter(safebook=link).all()
#     PasswordProtectedUsers.objects.filter(safebook=nu).all().delete()
#     IPUsers.objects.filter(safebook=nu).all().delete()



# def refreshflip(request,link):
#     quest=flipping.objects.filter(link=link).first()
#     print(quest)
#     if request.method =='POST':
#         deletepasswords(request,quest.id)
#         link = randlink()
#         quest.link= link
#         quest.ftime=datetime.now()
#         quest.dates=[]
#         quest.times=0
#         quest.save()
#         messages.success(request,"New link has been generated")
#         return redirect('../../view')
#     return render(request,'flipping/changelink.html',{"flink":quest})


# def durations(s):
#     print(1)
#     IST = pytz.timezone('Asia/Kolkata')
#     get_date = s.split()
#     year = get_date[0].split('-')
#     hourly_time = get_date[1].split(':')
#     y,mo,d= int(year[0]),int(year[1]),int(year[2])
#     h,mi,se = int(hourly_time[0]),int(hourly_time[1]),int(hourly_time[2])
#     start = datetime(y, mo, d, h, mi, se)        
#     now  = datetime.now(IST).replace(tzinfo=None)                         
#     dif_start =  str(start-now)
#     if dif_start[0] == '-':
#         return 1
