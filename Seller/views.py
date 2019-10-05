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


def loginValid(fun):
    def inner(request, *args, **kwargs):
        cookie_id = request.COOKIES.get("id")
        if cookie_id:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Seller/login/")
    return inner


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
                    response.set_cookie('images', user.photo)
                    return response
                else:
                    error_message = '密码错误'
            else:
                error_message = '邮箱不存在'
        else:
            error_message = '邮箱不能为空'

    return render(request, 'seller/login.html', locals())


def forgotPassword(request):
    return render(request, 'seller/ForgotPassword.html', locals())


@loginValid
def index(request):
    return render(request, 'seller/index.html', locals())


@loginValid
def personalInfo(request):
    user_id = int(request.COOKIES.get('id'))
    user = LoginUser.objects.get(id=user_id)
    # 如果请求方式为POST
    if request.method == 'POST':
        # 获取数据
        username = request.POST.get('username')
        phoneNumber = request.POST.get('phoneNumber')
        photo = request.FILES.get('photo')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        # 设置数据并保存
        user.username = username
        user.phoneNumber = phoneNumber
        user.photo = photo
        user.age = int(age)
        user.gender = gender
        user.address = address
        user.save()
    return render(request, 'seller/personalInfo.html', locals())


def goodsType(request):
    error_message = ''
    if request.method == 'POST':
        type_label = request.POST.get('type_label')
        type_description = request.POST.get('type_description')
        type_picture = request.FILES.get('type_picture')
        if type_label:
            if type_description:
                if type_picture:
                    type = GoodsType()
                    type.type_label = type_label
                    type.type_description = type_description
                    type.type_picture = type_picture
                    type.save()
                    error_message = '商品添加成功'
                else:
                    error_message = '商品类型图片不能为空'
            else:
                error_message = '商品类型描述不能为空'
        else:
            error_message = '商品类型名称不能为空'
    return render(request, 'seller/goodsType.html', locals())


def addGoods(request):
    error_message = ''
    goods_type_list = GoodsType.objects.all()
    if request.method == 'POST':
        goods_number = request.POST.get('goods_number')
        if goods_number:
            number = Good.objects.filter(goods_number=goods_number).first()
            if not number:
                goods = Good()
                goods.goods_number = goods_number
                goods.goods_name = request.POST.get('goods_name')
                goods.goods_price = request.POST.get('goods_price')
                goods.goods_count = request.POST.get('goods_count')
                goods.goods_location = request.POST.get('goods_location')
                goods.goods_safe_date = request.POST.get('goods_safe_date')
                goods.goods_pro_time = request.POST.get('goods_pro_time')
                goods.goods_status = request.POST.get('goods_status')
                # 保存外键类型
                goods_type_id = int(request.POST.get('goods_type'))
                goods.goods_type = GoodsType.objects.get(id=goods_type_id)
                # 保存图片
                goods_picture = request.FILES.get('goods_picture')
                goods.goods_picture = goods_picture
                # 保存卖家
                user_id = request.COOKIES.get('id')
                # 商品绑定的是登录账号的那个卖家
                goods.goods_store = LoginUser.objects.get(id=int(user_id))
                goods.save()
                error_message = '商品添加成功'
            else:
                error_message = '该商品已存在'
        else:
            error_message = '商品信息不完整'

    return render(request, 'seller/addGoods.html', locals())


from django.core.paginator import Paginator


def goodsList(request, num=10, status=1, page=1):
    page = int(page)
    if status == '1':
        goods = Good.objects.filter(goods_status=True)
    elif status == '0':
        goods = Good.objects.filter(goods_status=False)
    else:
        goods = Good.objects.all()
    all_goods = Paginator(goods, int(num))
    goods_list = all_goods.page(page)
    return render(request, 'seller/goodsList.html', locals())


def goods_status(request, status, id):
    id = int(id)
    status = status
    goods = Good.objects.filter(id=id).first()
    if status == '1':
        goods.goods_status = True
    else:
        goods.goods_status = False
    goods.save()
    url = request.META.get('HTTP_REFERER', '/Seller/goodsList/1/1/')
    return HttpResponseRedirect(url)


def storeInformation(request):
    return render(request, 'seller/storeInformation.html', locals())
# Create your views here.
