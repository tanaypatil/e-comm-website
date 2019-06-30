from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.


def rateart(request):
    print(Pairs.objects.count())
    return render(request, 'voting/rateart.html', context={'p': Pairs.objects.all()[0], 'count': Pairs.objects.count(), 'all': Pairs.objects.all()})


def vote(request):
    return render(request, 'voting/ratehome.html')


def addup(request):
    alt = request.POST['alt']
    print(alt)
    pid = request.POST['pid']
    print(pid)
    pnext = int(pid) + 1
    p = Pairs.objects.get(pid=pid)
    if p.alt_1 == alt:
        p.s1 += 1
    else:
        p.s2 += 1
    p.save()
    count = Pairs.objects.count()
    if int(pid) != count:
        print("h1")
        pn = Pairs.objects.get(pid=pnext).pid
    else:
        print("h2")
        pn = 0
    context = {
        'success': True,
        'message': 'success',
        'pn': pn
    }
    return JsonResponse(context)
