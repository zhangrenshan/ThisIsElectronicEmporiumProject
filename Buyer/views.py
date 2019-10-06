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
            user = BuyerUser.objects.filter(email=email).first()
            # 如果邮箱没有被占用
            if not user:
                password01 = request.POST.get('password01')
                password02 = request.POST.get('password02')
                # 如果密码一致
                if password01 == password02:
                    username = request.POST.get('username')
                    # 创建用户,保存信息
                    new_user = BuyerUser()
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
                    request.session['email'] = user.email
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


def logout(request):
    url = request.META.get("HTTP_REFERER", "/Buyer/index/")
    response = HttpResponseRedirect(url)
    for k in request.COOKIES:
        response.delete_cookie(k)
    del request.session['email']
    return response


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


@loginValid
def user_center_info(request):
    user_id = int(request.COOKIES.get('id'))
    user = BuyerUser.objects.get(id=user_id)
    if request.method == 'POST':
        phoneNumber = request.POST.get('phoneNumber')
        address = request.POST.get('address')
        if phoneNumber:
            user.phoneNumber = phoneNumber
            if address:
                user.address = address
        user.save()
    return render(request, 'buyer/user_center_info.html', locals())


@loginValid
def user_center_order(request):
    return render(request, 'buyer/user_center_order.html', locals())


@loginValid
def user_center_site(request):
    return render(request, 'buyer/user_center_site.html', locals())


import time
import datetime


@loginValid
def pay_order(request):
    goods_id = request.GET.get("goods_id")
    count = request.GET.get("count")
    if goods_id and count:
        # 保存订单表，但是保存总价
        order = PayOrder()
        order.order_number = str(time.time()).replace(".","")
        order.order_data = datetime.datetime.now()
        order.order_user = LoginUser.objects.get(id=int(request.COOKIES.get("id"))) #订单对应的买家
        order.save()
        # 保存订单详情
        # 查询商品的信息
        goods = Goods.objects.get(id=int(goods_id))
        order_info = OrderInfo()
        order_info.order_id = order
        order_info.goods_id = goods.id
        order_info.goods_picture = goods.goods_picture
        order_info.goods_name = goods.goods_name
        order_info.goods_count = int(count)
        order_info.goods_price = goods.goods_price
        order_info.goods_total_price = goods.goods_price*int(count)
        order_info.store_id = goods.goods_store     # 商品卖家，goods.goods_store本身就是一条卖家数据
        order_info.save()
        order.order_total = order_info.goods_total_price
        order.save()
    return render(request, "buyer/pay_order.html", locals())


@loginValid
def pay_order_more(request):
    data = request.GET
    data_item = data.items()
    request_data = []
    for key,value in data_item:
        if key.startswith("check_"):
            goods_id = key.split("_",1)[1]
            count = data.get("count_"+goods_id)
            request_data.append((int(goods_id),int(count)))
    if request_data:
        # 保存订单表，但是保存总价
        order = PayOrder()
        order.order_number = str(time.time()).replace(".","")
        order.order_data = datetime.datetime.now()
        order.order_user = LoginUser.objects.get(id=int(request.COOKIES.get("id")))     # 订单对应的买家
        order.save()
        # 保存订单详情
        # 查询商品的信息
        order_total = 0
        for goods_id,count in request_data:
            goods = Goods.objects.get(id=int(goods_id))
            order_info = OrderInfo()
            order_info.order_id = order
            order_info.goods_id = goods.id
            order_info.goods_picture = goods.goods_picture
            order_info.goods_name = goods.goods_name
            order_info.goods_count = int(count)
            order_info.goods_price = goods.goods_price
            order_info.goods_total_price = goods.goods_price*int(count)
            order_info.store_id = goods.goods_store     # 商品卖家，goods.goods_store本身就是一条卖家数据
            order_info.save()
            order_total += order_info.goods_total_price     # 总价计算
        order.order_total = order_total
        order.save()
    return render(request,"buyer/pay_order.html",locals())


@loginValid
def cart(request):
    return render(request, 'buyer/cart.html', locals())


from DjangoWork.settings import alipay_public_key_string,alipay_private_key_string
from alipay import AliPay


def AlipayViews(request):
    order_number = request.GET.get("order_number")
    order_total = request.GET.get("total")

    # 实例化支付
    alipay = AliPay(
        appid=2016101200667734,
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )
    # 实例化订单
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_number,  # 订单号
        total_amount=str(order_total),  # 支付金额，是字符串
        subject="生鲜交易",  # 支付主题
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",#结果返回的地址
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/" #订单状态发生改变后返回的地址
    )  # 网页支付订单

    # 拼接收款地址 = 支付宝网关+订单返回参数
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string

    return HttpResponseRedirect(result)
# Create your views here.
