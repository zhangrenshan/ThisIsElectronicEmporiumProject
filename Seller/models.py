from django.db import models


class LoginUser(models.Model):
    email = models.EmailField()                                             # 用户邮箱
    password = models.CharField(max_length=18)                              # 用户密码

    username = models.CharField(max_length=32)                              # 用户昵称
    phoneNumber = models.CharField(max_length=11, null=True, blank=True)    # 用户手机
    photo = models.ImageField(upload_to='images', null=True, blank=True)    # 用户头像
    age = models.IntegerField(null=True, blank=True)                        # 用户年龄
    gender = models.CharField(max_length=32, null=True, blank=True)         # 用户性别
    address = models.TextField(max_length=254, null=True, blank=True)       # 用户地址


class GoodsType(models.Model):
    type_label = models.CharField(max_length=32)            # 类型名称
    type_description = models.TextField()                   # 类型描述
    type_picture = models.ImageField(upload_to='images')    # 类型图片


class Good(models.Model):
    goods_number = models.CharField(max_length=11)          # 商品编号
    goods_name = models.CharField(max_length=32)            # 商品名称
    goods_price = models.FloatField()                       # 商品价格
    goods_count = models.IntegerField()                     # 商品数量
    goods_location = models.CharField(max_length=254)       # 商品产地
    goods_safe_date = models.IntegerField()                 # 商品保质期
    goods_pro_time = models.DateField(auto_now=True)        # 商品生产期
    goods_status = models.BooleanField(blank=True)          # 商品状态

    goods_description = models.TextField(default="好吃又好玩，偏偏还不贵")              # 商品描述
    goods_picture = models.ImageField(upload_to='images', blank=True, null=True)        # 商品照片
    goods_type = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE, default=1)   # 商品类型
    goods_store = models.ForeignKey(to=LoginUser, on_delete=models.CASCADE, default=1)  # 商品店铺


class ValidCode(models.Model):
    code_user = models.EmailField()                         # 验证码用户
    code_content = models.CharField(max_length=256)         # 验证码内容
    code_time = models.DateTimeField(auto_now=True)         # 验证码时间
    code_status = models.IntegerField(default=0)            # 验证码状态  1代表使用 0代表未使用
# Create your models here.
