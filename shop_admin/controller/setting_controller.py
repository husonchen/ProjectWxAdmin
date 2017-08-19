from django_url_framework.controller import ActionController
from shop_admin.model.log_change_money import LogShopMoney
from shop_admin.util.TplHelper import *
from shop_admin.model.shop_user import *
from shop_admin.model.mp_info import MpInfo
from django.shortcuts import render

class SettingController(ActionController):
    def lucky_money(self,request):
        user = request.session['user']
        rows = LogShopMoney.objects.filter(shop_id=user.shop_id).order_by('-id')[0:1]
        if len(rows) == 0:
            current_big = 0
        else :
            current_big = float(rows[0].money) / 100
        return getTpl({'user': user,'current_big':current_big}, 'setting/lucky_money')

    def change_money(self,request):
        user = request.session['user']
        try:
            money = int(float(request.GET['money']) * 100)
        except:
            return 'false'
        if money <= 0:
            return 'false'
        log = LogShopMoney(shop_id=user.shop_id,money=money)
        log.save()
        return 'true'

    def user_info(self,request):
        return getTpl({},'setting/user_info')

    def change_pass(self,request):
        user = request.session['user']
        ori_pass = request.GET['ori_pass']
        new_pass = request.GET['new_pass']
        shopUser = ShopUser.objects.filter(id=user.id).all()[0]
        if shopUser.password != ori_pass:
            return HttpResponse('false')
        else :
            ShopUser.objects.filter(id=user.id).update(password=new_pass)
            return HttpResponse("true")

    def media_platform(self,request):
        user = request.session['user']
        mps = MpInfo.objects.filter(shop_id=user.shop_id)
        return render(request, 'setting/media _platform.html', {'mp_list':mps})