from django_url_framework.controller import ActionController
from shop_admin.model.log_change_money import LogShopMoney
from shop_admin.util.TplHelper import *

class SettingController(ActionController):
    def lucky_money(self,request):
        user = request.session['user']
        rows = LogShopMoney.objects.filter(shop_id=user.shop_id).order_by('-id')[0:1]
        if len(rows) == 0:
            current_big = 0
        else :
            current_big = rows[0].money
        return getTpl({'user': user,'current_big':current_big}, 'setting/lucky_money')

    def change_money(self,request):
        user = request.session['user']
        try:
            money = float(request.GET['money'])
        except:
            return 'false'
        if money <= 0:
            return 'false'
        log = LogShopMoney(shop_id=user.shop_id,money=money)
        log.save()
        return 'true'