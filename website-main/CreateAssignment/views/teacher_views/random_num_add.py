from CreateAssignment.models import RandomNumber 
from django.http import JsonResponse


def RandomNumberAdd(request,link,qno):
    randoms = RandomNumber.objects.filter(question_id = qno)
    if len(randoms) == 5:
        return JsonResponse({
            "status": False,
            "msg": "You can not add more than 5 random variables."
        })
    try:
        float(request.POST["min_val"])
        float(request.POST["max_val"])
        bool(int(request.POST["integer_only"]))
    except:
        return JsonResponse({
            "status": False,
            "msg": "Please specify valid numbers in min_val and max_val."
        })

    RandomNumber.objects.create(
        question_id = qno,
        min_num = float(request.POST["min_val"]),
        max_num = float(request.POST["max_val"]),
        integers_only = bool(int(request.POST["integer_only"])),
        var_number = len(randoms)+1
    )

    return JsonResponse({
        "status": True,
        "var_num": len(randoms)+1,
        "min_val": request.POST["min_val"],
        "max_val": request.POST["max_val"],
        "integer_only": bool(int(request.POST["integer_only"])),

    })