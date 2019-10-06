from django.shortcuts import render
from django.http import HttpResponseRedirect
import hashlib
from Buyer.models import *
from Seller.models import *


def born(request):
    return render(request, 'buyer/born.html', locals())


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def loginValid(func):
    def inner(request, *args, **kwargs):
        cookie_id = request.COOKIES.get("id")
        if cookie_id:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")

    return inner


def base(request):
    return render(request, 'buyer/base.html', locals())


def registerBase(request):
    return render(request, 'buyer/register_base.html', locals())


def register(request):
    error_message = ''
    # 如果请求方式为POST
    if request.method == 'POST':
        email = request.POST.get('email')   # 此处'email'是前端html页面中的name
        # 如果邮箱不为空
        if email:
            user = LoginUser.objects.filter(email=email).first()
            # 如果邮箱没有被占用
            if not user:
                password01 = request.POST.get('password01')
                password02 = request.POST.get('password02')
                # 如果密码一致
                if password01 == password02:
                    username = request.POST.get('username')
                    # 创建用户,保存信息
                    new_user = LoginUser()
                    new_user.email = email
                    new_user.username = username
                    new_user.password = setPassword(password01)
                    new_user.save()
                    return HttpResponseRedirect('/Buyer/login/')
                else:
                    error_message = '密码不一致，请确认'
            else:
                error_message = '邮箱已被注册'
        else:
            error_message = '邮箱不能为空'

    return render(request, 'buyer/register.html', locals())


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
                    response = HttpResponseRedirect('/Buyer/index/')
                    response.set_cookie('email', user.email)
                    response.set_cookie('id', user.id)
                    return response
                else:
                    error_message = '密码错误'
            else:
                error_message = '邮箱不存在'
        else:
            error_message = '邮箱不能为空'

    return render(request, 'buyer/login.html', locals())


def forgotPassword(request):
    return render(request, 'buyer/ForgotPassword.html', locals())


@loginValid
def index(request):
    goods_type = GoodsType.objects.all()  # 获取所有类型
    result = []
    for ty in goods_type:
        # 按照生产日期对对应类型的商品进行排序
        goods = ty.goods_set.order_by("-goods_pro_time")
        if len(goods) >= 4:  # 进行条件判断
            goods = goods[:4]
            result.append({"type": ty, "goods_list": goods})
            print(result)

    return render(request, 'buyer/index.html', locals())


@loginValid
def detail(request, id):
    goods = Goods.objects.get(id=int(id))
    goods_recommend = Goods.objects.order_by('-goods_pro_time')[0:2]
    return render(request, 'buyer/detail.html', locals())

# Create your views here.
