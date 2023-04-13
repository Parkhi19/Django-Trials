from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
import json
import pytz
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import request,JsonResponse
from django.shortcuts import render,redirect
from django.views.generic.edit import DeleteView
from .models import questiondata
from django.views.generic import CreateView, UpdateView
import random
from createquiz.models import createlink
from django.contrib import messages
from .forms import UploadFileForm
from users.models import Profile,User
from student.models import st_data,result,instructions
from student.views import topThree
from users.views import isEmailVerified as ev

@login_required
def json_loader(request,link):
    if not ev(request):
        return redirect('email-verify')
        
    if True:
        codes_id= createlink.objects.filter(link=link).all()
        all_sections = []
        for code_id in codes_id:
            content = []
            dic = {}
            if code_id is not None :
                everyquestion = questiondata.objects.filter(link_id=code_id.id).all()
                num = 1
                for questiondatas in everyquestion:
                    questions = {}
                    options = {} 
                    i = 1

                    for type in questiondatas.options.split("/.\\"):
                        if type == '': 
                            continue
                        options['opt_'+str(i)] = type 
                        i += 1
                    questions["question"],questions["options"],questions["type"],questions["time"],questions["level"],questions["number"],questions["explanation"],questions["que_num"]  = questiondatas.question,options,questiondatas.type,questiondatas.time,questiondatas.level,questiondatas.id,questiondatas.explanation,num
                    questions["search"] = questiondatas.question.strip().replace(' ','+')
                    questions["img"] = str(questiondatas.photo)
                    content.append(questions)
                    num+=1
            dic = {"questions":content,"section":code_id.topic_name,"section_time":code_id.ttime}
            all_sections.append(dic)
        data_to_be_sent = {"Quiz_data":all_sections,"qtype":codes_id.first().qtype,"ttype":codes_id.first().ttype}
        return HttpResponse(json.dumps(data_to_be_sent))
    
    
@login_required
def home(request,link):  
    if not ev(request):
        return redirect('email-verify')
        
    codes_id= createlink.objects.filter(link=link).all()
    if codes_id is None:
        return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    t = Profile.objects.filter(user = request.user).first()
    all_sections = []
    for code_id in codes_id:
        content = []
        dic = {}
        if code_id is not None :
            everyquestion = questiondata.objects.filter(link_id=code_id.id).all()
            num = 1
            for questiondatas in everyquestion:
                questions = {}
                options = {} 
                i = 1

                for type in questiondatas.options.split('/.\\'):
                    if type == '':
                        continue
                    options['opt_'+str(i)] = type 
                    i += 1
                questions["question"],questions["options"],questions["type"],questions["time"],questions["level"],questions["number"],questions["explanation"],questions["que_num"]  = questiondatas.question,options,questiondatas.type,questiondatas.time,questiondatas.level,questiondatas.id,questiondatas.explanation.split("\n"),num
                questions["correct"] =  questiondatas.correct
                questions["search"] = questiondatas.question.strip().replace(' ','+')
                questions["img"] = str(questiondatas.photo)
                content.append(questions)
                num+=1
        dic = {"questions":reversed(content),"section":code_id.topic_name.replace("-"," "),"new_link":code_id.topic_name,"time":code_id.ttime}
        all_sections.append(dic)
    if t.type == 't':
        if codes_id.first().creator_id != request.user.id:
            return render(request,"public/something.html",{"msg":"This quiz doesn't belong to you. Please go back...","videos":topThree()})
        if request.method == 'POST':
            for code in codes_id:
                if code.topic_name == request.POST["as"]:
                    code.ttime = request.POST["ttime"]
                    code.save()
                    messages.success(request,"Time for "+str(code.ttime)+" updated successfully!")
                    continue
            return redirect('./')
        return render(request,"public/taker.html",{"sections":all_sections,"course":code_id.course_name.replace("-"," "),"ttype":code_id.ttype,"qtype":code_id.qtype})
    else:
        return redirect('./test')


@login_required
def settings(request,link):
    if not ev(request):
        return redirect('email-verify')
        
    codes= createlink.objects.filter(link =link).all()
    if codes.first() is None:
        return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    if request.user.id != codes.first().creator_id:
        return render(request,"public/something.html",{"msg":"You are not allowed on this page. Please go back.","videos":topThree()})
    if request.method == 'POST':
        # if request.method
        start = request.POST["start"].replace('T',' ')
        margin = request.POST["margin"].replace('T',' ')
        result = request.POST["result"].replace('T',' ')
        ajf =str(datetime.strptime(margin, '%Y-%m-%d %H:%M')-datetime.strptime(start, '%Y-%m-%d %H:%M'))
        if ajf[0] == '-' or ajf == '0:00:00':
            messages.error(request,'Last Login time can not be same or greater than the quiz start time')
            return redirect('./')
        if str(datetime.strptime(result, '%Y-%m-%d %H:%M')-datetime.strptime(margin, '%Y-%m-%d %H:%M'))[0] == '-':
            messages.error(request,'Result Opening time can not be greater than the Last Login time')
            return redirect('./')
        for code in codes:
            code.course_name = request.POST["course_name"]
            code.start = request.POST["start"]
            code.margin = request.POST["margin"]
            code.ttype = request.POST["ttype"]
            code.result_time = request.POST["result"]
            code.save()
        messages.success(request,"Settings Updated Successfully")
        return redirect('../')
    code = codes.first()
    start_v = str(code.start)[:10]+'T'+str(code.start)[11:16]
    end_v = str(code.margin)[:10]+'T'+str(code.margin)[11:16]
    res_t = str(code.result_time)[:10]+'T'+str(code.result_time)[11:16]
    data = {'course':code.course_name,'topic':code.topic_name,'start':start_v,'margin':end_v,"code_id":code.id,"result":res_t,"ttype":code.ttype}
    return render(request,'public/settings.html',data)


@login_required
def update_question(request,link,qno):
    if not ev(request):
        return redirect('email-verify')
        
    change = questiondata.objects.filter(id = qno).first()
    code = createlink.objects.filter(link = link).first()
    if code is None:
        return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    if request.user.id != code.creator_id:
        return render(request,"public/something.html",{"msg":"You are not allowed on this page. Please go back.","videos":topThree()})
    some = {}
    some["type"] = change.type
    some["level"] = change.level
    some["time"] = change.time
    some["question"] = change.question
    some["options"] = change.options.split("/.\\")
    some["correct"] = change.correct
    some["explanation"] = change.explanation
    some["img"] = change.photo

    if request.method == "POST":
        change.type = request.POST["type"]
        change.level= request.POST["level"]
        try:
            change.time = int(request.POST["time"])
        except:
            change.time = 60
        change.question = request.POST["question"]
        change.correct = request.POST["correct"]
        change.explanation = request.POST["explanation"]
        change.options = request.POST["options"]
        change.save()
        return redirect("../resu")
    return render(request,"public/edit.html",{"questiondata":some,"createlink":{"ttype":code.ttype}})

@login_required
def add_question(request,link,section):
    if not ev(request):
        return redirect('email-verify')
        
    code = createlink.objects.filter(link = link).first()
    if code is None:
        return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    if request.user.id != code.creator_id:
        return render(request,"public/something.html",{"msg":"You are not allowed on this page. Please go back.","videos":topThree()})
    if request.method == "POST":
        ct = 0
        change = questiondata()
        if request.POST["type"] == "" or request.POST["level"] == "" or request.POST["question"] == "" or request.POST["correct"] == "" or request.POST["explanation"] == "":
            messages.error(request,"Please fill all the fields!")
            a = {"type" : request.POST["type"],"level" : request.POST["level"],"time" : request.POST["time"],"question":request.POST["question"],"ttype":code.ttype,"correct":request.POST["correct"],"explanation":request.POST["explanation"],"options":request.POST["options"].split("/.\\")}
            return render(request,"public/new.html",a)
        
        change.type = request.POST["type"]     
        change.level= request.POST["level"]
        
        try:
            change.time = int(request.POST["time"])
        except:
            change.time = 60
        change.question = request.POST["question"]
        try:
            change.photo = request.FILES["photo"]
        except:
            ct =1
        change.correct = request.POST["correct"]
        change.explanation = request.POST["explanation"]
        if request.POST["type"] == "i":
            change.options = request.POST["options"]
        elif request.POST["options"] == "":
            messages.error(request,"Add atleast one option!")
            return render(request,"public/new.html")
        else:
            change.options = request.POST["options"]
        change.link_id = createlink.objects.filter(link =link).filter(topic_name=section).first().id
        change.save()
        return redirect("../")
    return render(request,"public/new.html",{"ttype":code.ttype})
    

@login_required
def delete_question(request,link,nu):
    if not ev(request):
        return redirect('email-verify')
        
    code = createlink.objects.filter(link = link).first()
    if code is None:
        return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    if request.user.id != code.creator_id:
        return render(request,"public/something.html",{"msg":"You are not allowed on this page. Please go back.","videos":topThree()})
    if request.method == 'POST':
        code = createlink.objects.filter(link=link).first()
        stuans = st_data.objects.filter(link_id = code.id).all()
        for response in stuans:
            all_questions = response.questions.split(',')
            all_answers = response.answer.split(',')
            ct = 0
            st = ''
            an = ''
            while ct<len(all_questions):
                if all_questions[ct] == str(nu):
                    ct+=1
                    continue
                st+= all_questions[ct]+','
                an+= all_answers[ct]+','
                ct+=1
            response.questions = st[:len(st)-1]
            response.answer = an[:len(an)-1]
            response.save()
        
        questiondata.objects.filter(id = nu).first().delete()
        return redirect('../resd')
    return render(request,'public/delete.html')

        

def duration(s,e):
    IST = pytz.timezone('Asia/Kolkata')
    get_date = s.split()
    year = get_date[0].split('-')
    hourly_time = get_date[1].split(':')
    y,mo,d= int(year[0]),int(year[1]),int(year[2])
    h,mi,se = int(hourly_time[0]),int(hourly_time[1]),int(hourly_time[2])
    start = datetime(y, mo, d, h, mi, se)        
    now  = datetime.now(IST).replace(tzinfo=None)                         
    dif_start =  str(now - start)
    get_margin = e.split()
    year = get_margin[0].split('-')
    hourly_time = get_margin[1].split(':')
    y,mo,d = int(year[0]),int(year[1]),int(year[2])
    h,mi,se = int(hourly_time[0]),int(hourly_time[1]),int(hourly_time[2])
    end = datetime(y, mo, d, h, mi, se)        
    now  = datetime.now(IST).replace(tzinfo=None)                         
    dif_end =  str(end - now)
    if dif_start[0] != '-' and dif_end[0] != '-':
        return 1
    if dif_start[0] == '-' and dif_end[0] != '-':
        return 2
    if dif_start[0] != '-' and dif_end[0] == '-':
        return 3
    else:
        return 4
        
           
@login_required
def update_name(request,link):
    if not ev(request):
        return redirect('email-verify')
        
    if request.method == "POST":
        if len(request.POST["first"]) < 1:
            messages.error(request,'Write something as your first Name to continue')
            return redirect('./')
        user = request.user
        user.first_name = request.POST["first"].upper()
        user.last_name = request.POST["last"].upper()
        user.save()
        return redirect('./instructions');
    return render(request,"public/update_name.html")
   
        
        
        
@login_required
def timechecker(request,link):
    if not ev(request):
        return redirect('email-verify')
        
    link_data= createlink.objects.filter(link =link).first()
    if link_data is None:
        return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    if request.user.profile.type == "t":
        return redirect("./")
    start_d = str(link_data.start).split('+')[0]
    margin_d = str(link_data.margin).split('+')[0]
    oc = duration(start_d,margin_d)
    if len(request.user.first_name) <=1:
        return redirect('./update-name')
    insts = []
    insta = instructions.objects.filter(link = link_data.id).first()
    if insta != None:
        inst = insta.instructions
        for each in inst.split("\n"):
            if len(each.strip()) < 1:
                continue
            insts.append(each)
    if oc == 1:
        if request.method == 'POST':
            codes = createlink.objects.filter(link =link).all()
            if codes.first().responses is not None:
                if str(request.user.id) in codes.first().responses.split():
                    return redirect('./test')
            for code in codes:
                code.t_responses += 1
                x = str(request.user.id)+'+'
                if code.responses == None or code.responses == '':
                    code.responses = x[:len(x)-1]
                else:
                    code.responses = code.responses+'+'+x[:len(x)-1]
                code.save()
            return redirect('./test')
        return render(request,'public/instructions.html',{"link":link,"given":["yze-bdxr-hmo","hyr-amzo-igc","tqz-nhvm-vid"],"endtime":margin_d,"inst":insts})
    elif oc == 2:
        return render(request,'public/instructions.html',{'msg':'Quiz has not started yet',"link":link,"given":["yze-bdxr-hmo","hyr-amzo-igc","tqz-nhvm-vid"],"time":start_d,"inst":insts})
    elif oc == 3:
        return render(request,'public/something.html',{'msg':'Quiz is over now, better luck next time',"videos":topThree()})
    else:
        return render(request,'public/something.html',{'msg':'Getting some error while loading please try later',"videos":topThree()})

@login_required
def refresh_page(request,link):
    if not ev(request):
        return redirect('email-verify')
        
    x = request.user.id
    code= createlink.objects.filter(link =link).first()
    data = st_data.objects.filter(username_id = request.user.id).filter(link_id = code.id).first()
    try:
        mi = data.id
    except:
        saving = st_data()
        saving.link_id = code.id
        saving.username_id = x
        saving.save()
        store = result()
        store.scores = '0'
        store.stans_id_id = st_data.objects.filter(username_id = int(x)).filter(link_id = code.id).first().id
        store.save()
        
        
@login_required
def st_answer(request,link):
    if not ev(request):
        return redirect('email-verify')
        
    code= createlink.objects.filter(link = link).first()
    
    #if there is no code with the given link
    if code == None:
        return render(request,"public/something.html",{"msg":"Please check you link again. You might be on wrong link","videos":topThree()})
    
    #if the user profile is a teacher type
    if request.user.profile.type == "t":
        return redirect("./")
    
    
    #if the quiz is restricted to institute and the email is nitj domain too
#     if code.institute == True and "@nitj.ac.in" not in request.user.email:
#         return render(request,"public/something.html",{"msg":"This test can only be given by people within the organisation. If you think it's a mistake contact your quiz taker.","videos":topThree()})
    
    # if student user id is not in code.responses
    if code.responses == None or code.responses == '' or str(request.user.id) not in code.responses.split('+'):
        return redirect('./instructions')
    
    #if student has already given the quiz than it would have some student data 
    student = st_data.objects.filter(link_id = code.id).filter(username_id = request.user.id).first()
    if str(request.user.id) in code.responses.split('+') and student is not None:
        return render(request,'public/something.html',{'msg':"Quiz can be given once only and you have already taken this quiz.","videos":topThree()})
    
    #if the time exceeds the last login time
    now = datetime.now().replace(tzinfo=None)
    last = code.margin.replace(tzinfo=None)
    if str(last-now)[0] == '-':
        code.responses = code.responses.replace('+'+str(request.user.id),'').replace(str(request.user.id),'')
        code.t_responses -= 1    
        code = code.save()
        return render(request,"public/something.html",{"msg":"The Quiz is over now","videos":topThree()})

    mydata = st_data()
    if request.method == 'POST':
        if st_data.objects.filter(link = code.id).filter(username_id = int(request.user.id)).first() != None:
            return render(request,"public/something.html",{"msg":"You have already submitted the result for this quiz. The previous quiz result is considered.","videos":topThree()})
        mydata.answer = request.POST["answer"]
        mydata.questions = request.POST["questions"]
        mydata.username_id = int(request.user.id)
        mydata.link_id = code.id
        mydata.save()
        return redirect('./res')    
    return render(request,'public/giver.html')


@login_required
def res(request,link):
    codes= createlink.objects.filter(link =link).all()
    y = st_data.objects.filter(link_id = codes.first().id).filter(username_id = int(request.user.id)).first()
    cor = []
    for que_no in y.questions.split(','):
        all_data = questiondata.objects.filter(id = int(que_no)).first()
        cor.append(all_data.correct)
    score = ''
    ans = y.answer.split(',')
    marks = 0
    for i in range(len(ans)):
        if ans[i] == cor[i]:
            score += '1,'
            marks += 1
        else:
            score += '0,'
    mina = result()
    mina.scores = score[:len(score)-1]
    mina.stans_id_id = y.id
    mina.save()
    for code in codes:
        if str(code.minima) == 'None' or str(code.minima) == '':
            code.minima = str(marks)
        else:
            code.minima = str(min(int(code.minima),marks))
        if str(code.maxima) == 'None' or str(code.maxima) == '':
            code.maxima = str(marks)
        else:
            code.maxima = str(max(int(code.maxima),marks))
                
        code.mean = "{:.2f}".format((code.mean*(code.t_responses-1) + marks) / (code.t_responses))
        code.save()
    return redirect('./feedback')


@login_required
def result_edit_update(request,link):
    code= createlink.objects.filter(link =link).first()
    ya = st_data.objects.filter(link_id = code.id).all()
    for y in ya:
        cor = []
        va =y.questions.split(',')
        if len(va) ==0:
            return render(request,'something.html',{'msg':'All Questions are removed now',"videos":topThree()})
        for que_no in va:
            try:
                all_data = questiondata.objects.filter(id = que_no).first()
                cor.append(all_data.correct)
            except:
                continue
        score = ''
        ans =y.answer.split(',')
        for i in range(len(cor)):
            if ans[i] == cor[i]:
                score += '1,'
            else:
                score += '0,'
        # questiondata.objects.filter(id = que_no).first().delete()
        mina = result.objects.filter(stans_id_id = y.id).first()
        mina.scores = score[:len(score)-1]
        mina.save()
    return redirect('./')

@login_required
def respect(request,link):
    code= createlink.objects.filter(link =link).first()
    ya = st_data.objects.filter(link_id = code.id).all()
    for y in ya:
        cor = []
        va =y.questions.split(',')
        if len(va) ==0:
            return render(request,'something.html',{'msg':'All Questions are removed now',"videos":topThree()})
        for que_no in va:
            try:
                all_data = questiondata.objects.filter(id = int(que_no)).first()
                cor.append(all_data.correct)     
            except:
                continue
        score = ''
        ans =y.answer.split(',')
        for i in range(len(cor)):
            if ans[i] == cor[i]:
                score += '1,'
            else:
                score += '0,'
        mina = result.objects.filter(stans_id_id = y.id).first()
        mina.scores = score[:len(score)-1]
        mina.save()
    return redirect('./')
@login_required
def add_section(request,link):
    if not ev(request):
        return redirect('email-verify')
        
    all_sections = createlink.objects.filter(link=link).all()
    if all_sections.first() is None:
        return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    firstsection = all_sections.first()
    if request.method == "POST":
        cond = True
        for i in all_sections:
            if request.POST["topic_name"] == i.topic_name:
                cond = False
                messages.error(request,"A section with this name already exist")
                break
        if cond:
            add = createlink()
            add.link = firstsection.link
            add.creator_id = firstsection.creator_id
            add.course_name = firstsection.course_name.strip().replace(" ","-")
            add.start = firstsection.start
            add.margin = firstsection.margin
            add.mean = 0.0
            add.result_time = firstsection.result_time
            add.qtype = firstsection.qtype
            add.ttype = firstsection.ttype
            ct = 0
            for i in list(request.POST.items()):
                if  ct == 0:
                    ct+=1
                    continue
                if ct == 1:
                    add.topic_name = str(i[1]).strip().replace(" ","-") 
                if ct == 2:
                    add.ttime = str(i[1])
                ct+=1
            add.save()
            return redirect("../")
    return render(request,"createquiz/add_section.html",{"msg":firstsection.ttype})



@login_required
def instructs(request,link):
    if not ev(request):
        return redirect('email-verify')
    code = createlink.objects.filter(link=link).first()
    if(code.creator != request.user):
        return render(request,"public/something.html",{"msg":"This page doesn\'t belong to you."})
    insts = []
    inst = instructions.objects.filter(link = code.id).first().instructions
    for each in inst.split("\n"):
        if len(each.strip()) < 1:
            continue
        insts.append(each)
    return render(request,"public/instructions.html",   {"link":link,"endtime":code.margin,"inst":insts})


def leaderboard(request,link):
    response = {}
    if not request.user.is_authenticated:
        response = {"status": False}
    else:
        quiz = createlink.objects.filter(link = link).count()
        print(link,quiz)
        student_answers = st_data.objects.filter(link = quiz).all()
        data = []
        for student_answer in student_answers:
            student_result = result.objects.filter(stans_id = student_answer).first()
            marks = 0
            for each in student_result.score.split("+"):
                marks+=int(each)
            data.append(
                {
                    "name": student_answer.username.username,
                    "score": marks,
                }
            )
        response = {
            "status": True,
            "data": data,
        
        }
    return render(request,"public/leaderboard.html",{"response": response})