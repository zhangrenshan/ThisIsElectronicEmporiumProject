from django.shortcuts import render


def born(request):
    return render(request, 'Buyer/born.html', locals())
# Create your views here.
