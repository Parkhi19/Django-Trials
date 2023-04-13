from CreateAssignment.models import Question, QueImg
from django.http import JsonResponse
import json
from .profile_check import ProfileCheck


def QuestionAddImage(request,link,qno):
    chk=ProfileCheck(request,link)
    if chk ==1:
        img_box = QueImg.objects.create(question_id = qno,image = request.FILES["img"])
        print(img_box.id)
        question = Question.objects.filter(id = qno).first()
        order = json.loads(question.order)
        order.append({
            "type": "i",
            "id": img_box.id
        })
        question.order = json.dumps(order)
        question.save()
        return JsonResponse({
            "status": True,
            "id": img_box.id,
            "address": str(img_box.image) 
        })



