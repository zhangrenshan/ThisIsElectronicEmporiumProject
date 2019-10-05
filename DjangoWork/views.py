from django.shortcuts import render


def base(request):
    return render(request, 'base.html', locals())

# Create your views here.