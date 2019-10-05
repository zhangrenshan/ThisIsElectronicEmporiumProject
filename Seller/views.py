from django.shortcuts import render


def born(request):
    return render(request, 'Seller/born.html', locals())


def base(request):
    return render(request, 'Seller/base.html', locals())


def registerBase(request):
    return render(request, 'Seller/register_base.html', locals())
# Create your views here.
