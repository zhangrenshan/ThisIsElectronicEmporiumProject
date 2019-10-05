from django.shortcuts import render


def born(request):
    return render(request, 'Buyer/born.html', locals())


def base(request):
    return render(request, 'Buyer/base.html', locals())


def registerBase(request):
    return render(request, 'Buyer/register_base.html', locals())
# Create your views here.
