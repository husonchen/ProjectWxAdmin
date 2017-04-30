# encoding=utf-8
from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from shop_admin.model.order_ids import OrderIds

class DashboardController(ActionController):

    def index(self,request):
        # if request.session.has_key('user') is False:
        #     return HttpResponseRedirect('/login/')
        user = request.session['user']
        c = {"userName":user.shop_name}
        # return getTpl(c,'dashboard/index')
        return render(request, 'dashboard/index.html', c)

    def upload_ids(self,request):
        if request.method == 'POST':
            user = request.session['user']
            myfile = request.FILES
            content = myfile['myfile'].read()
            # print content
            querysetlist = []
            lines = content.split('\r\n')
            for line in lines[1:len(lines)]:
                if line == '':
                    continue
                querysetlist.append(OrderIds(order_id=line,shop_id=user.shop_id,create_time=None))
            OrderIds.objects.bulk_create(querysetlist,500)
            return 'OK'
        return 'Not Ok'