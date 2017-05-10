# encoding=utf-8
from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from shop_admin.model.order_ids import OrderIds
from shop_admin.model.shop_setting import ShopSetting

class DashboardController(ActionController):

    def index(self,request):
        # if request.session.has_key('user') is False:
        #     return HttpResponseRedirect('/login/')
        user = request.session['user']
        try:
            last_id = OrderIds.objects.filter(shop_id=user.shop_id).order_by('-create_time')[0]
            last_time = last_id.create_time
            num = OrderIds.objects.filter(shop_id=user.shop_id,create_time=last_time).count()
        except :
            last_time = ''
            num = 0
        try:
            shopSetting = ShopSetting.objects.filter(shop_id=user.shop_id)[0]
        except IndexError:
            shopSetting = ShopSetting(shop_id=user.shop_id,update_time=None)
            shopSetting.save()
        c = {"userName":user.shop_name,'last_time':last_time,'last_num':num,'shop_setting':shopSetting}
        # return getTpl(c,'dashboard/index')
        return render(request, 'dashboard/index.html', c)

    def upload_ids(self,request):
        if request.method == 'POST':
            user = request.session['user']
            myfile = request.FILES
            if myfile.has_key('myfile') == False:
                return 'not ok'
            content = myfile['myfile'].read()
            lines = content.split('\r\n')
            id_list = []
            for line in lines[1:len(lines)]:
                if line == '':
                    continue
                id_list.append(line)
            OrderIds().batchInsert(id_list,user.shop_id)
            return 'OK'
        return 'Not Ok'

    def change_flag(self,request):
        flag = request.GET['flag']
        value = request.GET['value']
        if value == 'True':
            value = True
        else:
            value = False
        user = request.session['user']
        shopSetting = ShopSetting.objects.get(shop_id=user.shop_id)
        if flag == 'filter_orderid':
            shopSetting.filter_orderid_flag=value
        elif flag == 'auto_pass':
            shopSetting.auto_pass_flag = value
        shopSetting.save()
        return 'True'
