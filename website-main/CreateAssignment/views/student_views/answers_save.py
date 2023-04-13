from django.http import JsonResponse
from CreateAssignment.models import *
from django.contrib.auth.decorators import login_required
import json
import math

def sqrt_check(x):
    while x.find('sqrt(') != -1:
        i = x.find('sqrt(')+5
        num = 0
        while i<len(x) and x[i] != ')':
            num = num*10 + int(x[i])
            i+=1
        x = x.replace('sqrt('+str(num)+')',str(math.sqrt(num)))
    return x


@login_required
def SaveStudentAnswer(request,link):
    assignment = CreateLink.objects.filter(link = link).first()
    data = json.loads(request.POST["data"])
    score = 0
    for each in data:
        student_answer = StudentAnswer.objects.filter(subquestion_id = each["sq_id"]).filter(user = request.user).first()
        sq = student_answer.subquestion
        randoms = StudentRandom.objects.filter(user = request.user).filter(question_id = sq.question_id).first()
        student_answer.answer = each["answer"]
        student_answer.save()
        ra = sq.answer
        j = 1
        for i in json.loads(randoms.randoms):
            ra = ra.replace("<var"+str(j)+">",str(i))
            j+=1
        try:
            # ra = sqrt_check(ra)
            correct_answer = eval(ra)
            ma = float(each["answer"])
            if float(abs(abs(correct_answer-ma)*100/ma)) <= float(sq.tollerance):
                student_score = StudentScore.objects.filter(user = request.user).filter(link  = assignment).first()
                student_score.score += (sq.score-student_answer.score)
                score = student_score.score
                student_answer.score = sq.score
                student_answer.save()
            else:
                if student_answer.score != 0:
                    student_score = StudentScore.objects.filter(user = request.user).filter(link  = assignment).first()
                    student_score.score -= (student_answer.score)
                    score = student_score.score
                    student_score.save()
                student_answer.score = 0
                student_answer.save()
            student_answer.save()
        except:
            pass
        student_answer.save()
    return JsonResponse({
        "status": True,
        "score": score,
    })

'''
    [
        {
            sq_id : 55,
            answer: "124",
        },
        {
            sq_id : 56,
            answer: "134",
        },
    ]
    
'''