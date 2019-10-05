from django.shortcuts import render


def born(request):
    return render(request, 'Seller/born.html', locals())
# Create your views here.
