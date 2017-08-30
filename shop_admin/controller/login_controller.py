from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from shop_admin.model.shop_user import ShopUser
from shop_admin.model.shop_setting import ShopSetting
from shop_admin.model.shop_account import ShopAccount
from shop_admin.model.log_change_money import LogShopMoney
from ProjectWx_admin.settings import SUPER_PASS
from shop_admin.wx.wx_utils import createTag
from django.shortcuts import render
from django.db import transaction
import traceback


class LoginController(ActionController):

    def hello(self,request):
        print("hello")
        for user in ShopUser.objects.all():
            print user
        return getTpl({},'login/hello')

    def index(self,request):
        if 'user' in request.session:
            del request.session['user']
        return getTpl({},'login/login')

    def login(self,request):
        password = request.GET['password']
        username = request.GET['username']

        try :
            if SUPER_PASS == None or password != SUPER_PASS :
                user = ShopUser.objects.get(user_name=username, password=password, del_flag=False)
            else :
                user = ShopUser.objects.get(user_name=username, del_flag=False)
        except :
            return HttpResponse("false")

        seting = ShopSetting.objects.get(shop_id=user.shop_id)
        user.shop_name = seting.name
        user.pay = seting.pay
        request.session['user'] = user
        return HttpResponse("true")

    def add_user(self,request):
        username = request.GET['username']
        password = request.GET['password']
        shopname = request.GET['shopname']
        try:
            with transaction.atomic():
                shopSetting = ShopSetting.objects.all().order_by('-shop_id')[0]
                shop_id = shopSetting.shop_id + 1
                ShopSetting(shop_id=shop_id,name=shopname, namespace='0').save()
                ShopUser(shop_id=shop_id,user_name=username,password=password).save()
                ShopAccount(shop_id=shop_id, balance=0).save()
                LogShopMoney(shop_id=shop_id,money=200 ).save()
                tagid = createTag('shop_%d' % shop_id,0)
                ShopSetting.objects.filter(shop_id=shop_id).update(wx_tag_id=tagid)
        except:
            traceback.print_exc()
            return HttpResponse("false")

        return HttpResponse("true")


    def register(self,request):
        if 'user' in request.session:
            del request.session['user']
        return render(request, 'login/register.html', {})