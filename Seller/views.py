from django.shortcuts import render
from django.http import HttpResponseRedirect
from Seller.models import *
import hashlib


def born(request):
    return render(request, 'seller/born.html', locals())


def base(request):
    return render(request, 'seller/base.html', locals())


def registerBase(request):
    return render(request, 'seller/register_base.html', locals())


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def register(request):
    error_message = ''
    # 如果请求方式为POST
    if request.method == 'POST':
        email = request.POST.get('email')       # 此处'email'是前端html页面中的name
        # 如果邮箱不为空
        if email:
            user = LoginUser.objects.filter(email=email).first()
            # 如果邮箱没有被注册
            if not user:
                password01 = request.POST.get('password01')
                password02 = request.POST.get('password02')
                # 如果两次密码一致
                if password01 == password02:
                    username = request.POST.get('username')
                    # 创建用户，保存信息
                    new_user = LoginUser()
                    new_user.email = email
                    new_user.password = setPassword(password01)
                    new_user.username = username
                    new_user.save()
                    return HttpResponseRedirect('/Seller/login/')
                else:
                    error_message = '密码不一致，请确认'
            else:
                error_message = '邮箱已被注册'
        else:
            error_message = '邮箱不能为空'
    return render(request, 'seller/register.html', locals())


def login(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                password = request.POST.get('password')
                db_password = user.password
                if db_password == setPassword(password):
                    response = HttpResponseRedirect('/Seller/index/')
                    response.set_cookie('email', user.email)
                    response.set_cookie('id', user.id)
                    return response
                else:
                    error_message = '密码错误'
            else:
                error_message = '邮箱不存在'
        else:
            error_message = '邮箱不能为空'

    return render(request, 'seller/login.html', locals())


def index(request):
    return render(request, 'seller/index.html', locals())
# Create your views here.
