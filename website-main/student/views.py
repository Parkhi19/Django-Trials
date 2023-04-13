from datetime import datetime
import pytz
import sys
from users.models import Profile,User
from django.http import request
from createquiz.models import createlink
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import result, st_data, errors, feedbackQue, feedbackAnswers, instructions
from django.views.generic import CreateView
from createquiz.models import createlink,feedback
from quiz.models import questiondata
from exam.models import talks 
from users.views import isEmailVerified as ev

# Create your views here.

def topThree():
    those = talks.objects.all()
    x = 3
    ret = []
    for each in reversed(those):
        if x:
            if(each.embed != ''):
                ret.append(each.embed)
                x-=1
            else:
                continue
        else:
            break
    return ret

def temppage(request):
    return render(request,"student/countdown.html")

def checktime(date_string):
    IST = pytz.timezone('Asia/Kolkata')
    date_string = str(date_string)[:19]
    # print(date_string)
    x = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')- datetime.now(IST).replace(tzinfo=None)
    # print(x)
    if str(x)[0] == "-":
        #should not be visible
        return True
    else:
        #should be visible
        return False
    # return 0

@login_required
def individual_result(request,link):
    if not ev(request):
        return redirect('email-verify')
    content = []
    code_id= createlink.objects.filter(link=link).first()
    if request.user.profile.type == "t":
        return redirect("./")
    if not checktime(code_id.result_time):
        return render(request,"public/something.html",{"msg":"Result for this quiz will be declared soon ...","videos":topThree()})
    if code_id is not None :
        studentdata = st_data.objects.filter(link_id = code_id.id).filter(username_id = (int(request.user.id))).first()
        re = result.objects.filter(stans_id_id = studentdata.id).first()
        score = re.scores.split(',') 
        question_numbers = studentdata.questions.split(',')
        total_marks = 0
        for i in score:
            total_marks+= int(i)
        num = 1
        your = studentdata.answer.split(',')
        for i in question_numbers:
            questions ={}
            everyquestion = questiondata.objects.filter(id=i).first()
            options = {} 
            m = 1

            try:
                for type in everyquestion.options.split('/.\\'):
                    if type == '':
                        continue
                    options['opt_'+str(m)] = type 
                    m += 1
                questions["question"],questions["options"],questions["type"],questions["time"],questions["number"],questions["explanation"],questions["que_num"],questions['correct'],questions['score']  = everyquestion.question,options,everyquestion.type,everyquestion.time,everyquestion.id,everyquestion.explanation.split("\n"),num,everyquestion.correct,score[num-1]
                questions["your"] = your[num-1]
                questions["img"] = str(everyquestion.photo)
                content.append(questions)
                num+=1
            except:
                continue
        
        t=Profile.objects.filter(user=request.user).first()
        all_questions = { "ques" : content,"total_marks":total_marks,"tot_ques":num-1,"stu_data_id": studentdata.id,"videos":topThree()}
        return render(request,'student/test.html',all_questions)
    
@login_required
def feedback_fun(request,link):
    if not ev(request):
        return redirect('email-verify')
    code_s= createlink.objects.filter(link =link).first()
    I = st_data.objects.filter(username_id = request.user.id).filter(link_id = code_s.id).first()
    if code_s.creator_id == request.user.id:
        return render(request,"student/feedback_info.html",)
    if I is None:
        return render(request,"public/something.html",{"msg":"Feedback for a test can only be given after the test. Please go through the test."})
    if feedbackAnswers.objects.filter(link = code_s).filter(user = request.user).first() is not None:
        return render(request,"public/something.html",{"msg":"You have already responded to this page"})
    all = feedbackQue.objects.filter(link = code_s.id).all()
    score = result.objects.filter(stans_id_id = I.id).first()
    marks = 0
    questions = 0
    attempted = 0
    un = 0
    for i in I.answer.split(","):
        if i != "":
            attempted+=1
        else:
            un+=1  
    for i in score.scores.split(','):
        marks+= int(i)
        questions += 1
    if request.method == "POST":
        ans = request.POST["answers"]
        at = False
        for each in ans.split('+'):
            if each != '':
                # messages.error(request,"Please answer all the questions")
                at = True
                break
        if not at:
            return redirect('quizzes')
        st = "-1+-2+"
        for each in all:
            st+= str(each.id) + "+"
            each.id
        A = feedbackAnswers()
        A.questions = st[:len(st)-1]
        A.answers = request.POST["answers"]
        A.link = code_s
        A.user = request.user
        A.save()
        return render(request,"public/something.html",{"msg":"Thank you for your valuable feedback."})
    return render(request,"public/feedback.html",{'marks':marks,'questions':questions,"pl":code_s.qtype,"videos":topThree(),"attempted":attempted,"un":un,"opening":code_s.result_time,"all":all})

def feedbackdata(link):
    feed = feedbackAnswers.objects.filter(link = link).all()
    A = []
    for each in feed:
        A.append({"name":each.user.username,"answers":each.answers.split('+')})
    B = ["Difficulty Level","Time Sufficency"]
    for each in feedbackQue.objects.filter(link = link).all():
        B.append(each.question)
    return {"ans":A,"que":B}

@login_required
def combined_result(request,link):
    if not ev(request):
        return redirect('email-verify')
    codes = createlink.objects.filter(link = link).all()
    # code = codes.first()
    if codes == None:
        return render(request,"public/something.html",{"msg":"The Quiz you are searching for doesnot exist"})
    if request.user.is_superuser:
        if codes.first().creator_id != request.user.id :
            return render(request,"public/something.html",{"msg":"This quiz does not belong to you so you cannot see the result"})
    RETURN = [] 
    MAR = []
    for code in codes:
        data = st_data.objects.filter(link_id = codes.first().id).all()
        qnums =questiondata.objects.filter(link_id = code.id).all()
        leng = 0
        for each in qnums:
            leng += 1
        A = []
        MAS = []
        num = 0
        for i in data:
            resu = result.objects.filter(stans_id = i.id).first()
            student = User.objects.filter(id = i.username_id).first()
            pro = Profile.objects.filter(user_id = student.id).first()
            if resu == None or student == None or pro == None:
                continue
            Z = resu.scores.split(",")
            X = i.questions.split(",")
            Y = i.answer.split(",")
            MAIN =[]
            mark =0
            for eachq in qnums:
                ideach = eachq.id
                check = True
                for itr in range(len(X)):
                    if X[itr] == str(ideach):
                        check =False
                        MAIN.append(Y[itr])
                        mark += int(Z[itr])
                if check:
                    MAIN.append("-")
            num+=1
            MAS.append(mark)
            try:
                A.append({"main": MAIN ,"num":num,"marks":mark,"name":student.first_name +' '+ student.last_name,"mail":student.email,"rollno":pro.roll_no})
            except:
                A.append({"main": MAIN ,"num":num,"marks":mark,"name":student.first_name +' '+ student.last_name,"rollno":"Not Mentioned"})
        MAR.append(MAS)
        questions = questiondata.objects.filter(link_id = code.id).all()
        ALLQUE = []
        corr = []
        diff = []
        for eachone in questions:
            ALLQUE.append(eachone.question)
            corr.append(eachone.correct)
            diff.append(eachone.level)
        RETURN.append({"main":A,"que":ALLQUE ,"corr":corr,"diff":diff,"heading":code.topic_name,"max_marks":leng})
    F = feedbackdata(codes.first().id)
    print(F)
    send = []
    for j in range(len(MAR[0])):
        temp = []
        num = 0
        for i in MAR:
            num +=1
            temp.append({i[j]})
        send.append(temp)
    return render(request,"student/full.html",{"main":RETURN,"feed":F,"tot":codes.first().course_name,"send":send})

    



def error_404(request,exception):
    return render(request,'student/error_404.html')

def error_500(request):
    type_, value, traceback = sys.exc_info()
    error = errors()
    error.page = request.get_full_path()
    error.head = str(type_)
    error.text = str(value)
    error.save()
    return render(request,'student/error_500.html')

def error_400(request,exception):
    return render(request,'student/error_400.html')

def error_403(request,exception):
    return render(request,'student/error_403.html')

@login_required
def render_feed(request,link):
    if not ev(request):
        return redirect('email-verify')
    code_s = createlink.objects.filter(link = link).first()
    if code_s.creator != request.user:
        return render(request,"public/something.html",{"msg":"This quiz doesn't belong to you. You might be on wrong link"})
    obj = feedbackQue.objects.filter(link = code_s).all()
    a = instructions.objects.filter(link = code_s.id).first()
    if a == None:
        b = instructions()
        b.instructions = ""
        b.link_id = code_s.id
        b.save()
        a = instructions.objects.filter(link = code_s.id).first()
    print(a)
    return render(request,"feed/all.html",{"all":obj,"inst":a})

@login_required
def instructions_update(request,link):
    if not ev(request):
        return redirect('email-verify')
    inst = instructions.objects.filter(link =createlink.objects.filter(link = link).first()).first()
    if request.method == "POST":
        inst.instructions = request.POST["instructions"]
        inst.save()
        return redirect("./feed")
    return redirect("./feed")


@login_required
def add_feed(request,link):
    if not ev(request):
        return redirect('email-verify')
    code_s = createlink.objects.filter(link = link).first()
    if code_s.creator != request.user:
        return render(request,"public/something.html",{"msg":"This quiz doesn't belong to you. You might be on wrong link"})
    if request.method == 'POST':
        if request.POST["question"] == '':
            messages.error('Write something in question to continue!')
            return render(request,"feed/add.html")
        fee = feedbackQue()
        fee.link = code_s #createlink.objects.filter(link =link).first().id
        fee.question = request.POST["question"]
        fee.options = request.POST["options"]
        fee.type_que = request.POST["type_que"]
        fee.save()
        return redirect("./feed")
    return render(request,"feed/add.html")
@login_required
def delete_feed(request,link,it):
    if not ev(request):
        return redirect('email-verify')
    code_s = createlink.objects.filter(link = link).first()
    if code_s.creator != request.user:
        return render(request,"public/something.html",{"msg":"This quiz doesn't belong to you. You might be on wrong link"})
    all = feedbackAnswers.objects.filter(link = code_s).all()
    for each in all:
        some = each.questions.split('+')
        string = ""
        answersup = ""
        ct = 0
        ft = each.answers.split('+')
        for one in some:
            if str(one) == str(it):
                ct+=1
                continue
            string += one + "+"
            answersup += ft[ct] +"+" 
            ct+=1
        print(it,answersup,string)
        # if(len(string)-1 == ct):

        each.answers = answersup[:len(answersup)-1]
        each.questions = string[:len(string)-1]
        each.save()
    feedbackQue.objects.filter(id=it).first().delete()
    return redirect("../feed")
@login_required
def edit_feed(request,link,it):
    if not ev(request):
        return redirect('email-verify')
    fee = feedbackQue.objects.filter(id = it).first()
    code_s = createlink.objects.filter(link = link).first()
    if code_s.creator != request.user:
        return render(request,"public/something.html",{"msg":"This quiz doesn't belong to you. You might be on wrong link"})
    if request.method == 'POST':
        if request.POST["question"] == '':
            messages.error('Write something in question to continue!')
            return render(request,"feed/add.html")
        fee.link = createlink.objects.filter(link = link).first() #createlink.objects.filter(link =link).first().id
        fee.question = request.POST["question"]
        fee.options = request.POST["options"]
        fee.type_que = request.POST["type_que"]
        fee.save()
        return redirect("../feed")
    return render(request,"feed/edit.html",{"it": fee})
