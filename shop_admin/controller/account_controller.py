from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from shop_admin.model.shop_account import ShopAccount
from shop_admin.model.charge_history import ChargeHistory
from django.http import  HttpResponseRedirect
import math

class AccountController(ActionController):

    def index(self,request):
        user = request.session['user']
        shopId = user.shop_id
        account = ShopAccount.objects.filter(shop_id=shopId, del_flag=False).all()[0]
        historys = ChargeHistory.objects.filter(shop_id=shopId).order_by('-create_time')[0:10]
        num = ShopAccount.objects.filter(shop_id=shopId, del_flag=False).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'account':account,'historys': historys, 'pageNum': pageNum}, 'account/index')

    def charge_money(self,request):
        return getTpl({},'account/add_money')

    def qrcode(self,request):
        user = request.session['user']
        shopId = user.shop_id
        return getTpl({'shop_id':shopId},'account/qrcode')
