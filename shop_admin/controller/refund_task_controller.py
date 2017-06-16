from django_url_framework.controller import ActionController
from django.shortcuts import render
from shop_admin.util.TplHelper import *
from shop_admin.model.user_upload import UserUpload
from shop_admin.model.verify_refund import VerifyRefund
from shop_admin.model.log_change_money import LogShopMoney
from shop_admin.model.shop_account import ShopAccount
from django.db.models import F
from django.db.models import Q
from shop_admin.nsq_producer.reject_notify_producer import RejectNotifier
import json
import math
# from django.db import connection
pageSize = 50

rejectNotify = RejectNotifier()

class RefundTaskController(ActionController):

    def task(self,request):
        user = request.session['user']
        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId,del_flag=False,verify_flag=0).order_by('id')[0:pageSize]
        num = UserUpload.objects.filter(shop_id=shopId,del_flag=False,verify_flag=0).count()
        pageNum = math.ceil(float(num)/pageSize)
        return render(request, 'refund_task/task.html', {'uploads':uploads,'pageNum':pageNum})


    def task_table(self,request):
        page = int(request.GET['page'])
        user = request.session['user']
        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId,del_flag=False,verify_flag=0).order_by('id')[(page-1)*pageSize:page*pageSize]
        num = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=0).count()
        pageNum = math.ceil(float(num) / pageSize)
        return render(request, 'refund_task/task_table.html', {'uploads':uploads,'pageNum':pageNum})

    def submit(self,request):
        user = request.session['user']
        id = request.GET['id']
        passFlag = request.GET['passFlag']
        if passFlag == '1':
            verify_flag = 1
            accept_flag = 0
        else:
            verify_flag = 2
            accept_flag = 1

        # if pass, check money
        if verify_flag == 1:
            #check money
            logMoney = LogShopMoney.objects.filter(shop_id=user.shop_id).order_by('-id')[0]
            effectRows = ShopAccount.objects.filter(shop_id=user.shop_id,balance__gte=logMoney.money,del_flag=False).\
                update(balance=F('balance') - logMoney.money)
            effectRows = UserUpload.objects.filter(id=id, shop_id=user.shop_id, verify_flag=0). \
                update(verify_flag=verify_flag, accept_flag=accept_flag)
            if effectRows == 0:
                return HttpResponse("no_money")
            upload = UserUpload.objects.filter(id=id)[0]
            v = VerifyRefund(shop_id=user.shop_id, open_id=upload.open_id, order_id=upload.order_id,
                             money=logMoney.money, update_time=None, create_time=None)
            v.save()
        else:
            effectRows = UserUpload.objects.filter(id=id,shop_id=user.shop_id,verify_flag=0).\
                    update(verify_flag=verify_flag,accept_flag=accept_flag)
            # notify client
            rejectNotify.pub_message([id])
            if effectRows == 0:
                return HttpResponse("false")
        return HttpResponse("true")

    def submit_batch(self,request):
        user = request.session['user']
        ids = json.loads(request.POST['ids'])
        passFlag = request.POST['passFlag']
        if passFlag == '1':
            verify_flag = 1
            accept_flag = 0
        else:
            verify_flag = 2
            accept_flag = 1
        id_num = len(ids)
        if verify_flag == 1:
            #check money
            logMoney = LogShopMoney.objects.filter(shop_id=user.shop_id).order_by('-id')[0]
            effectRows = ShopAccount.objects.filter(shop_id=user.shop_id,balance__gte=id_num * logMoney.money,del_flag=False).\
                update(balance=F('balance') - id_num * logMoney.money)
            if effectRows == 0:
                return HttpResponse("no_money")
            effectRows = UserUpload.objects.filter(id__in=ids,shop_id=user.shop_id,verify_flag=0).\
                    update(verify_flag=verify_flag,accept_flag=accept_flag)
            # print connection.queries
            if effectRows == 0:
                return HttpResponse("false")
            uploads = UserUpload.objects.filter(id__in=ids).all()
            vrs = []
            for upload in uploads:
                v = VerifyRefund(shop_id=user.shop_id, open_id=upload.open_id, order_id=upload.order_id,
                                 money=logMoney.money, update_time=None, create_time=None)
                vrs.append(v)
            VerifyRefund.objects.bulk_create(vrs)
        else:
            effectRows = UserUpload.objects.filter(id__in=ids, shop_id=user.shop_id, verify_flag=0).all()
            orderIds = []
            for row in effectRows:
                orderIds.append(row.order_id)
            rejectOrderIds = UserUpload.objects.filter(accept_flag = 1,order_id__in = orderIds,verify_flag=2).\
                update(del_flag=1)
            effectRows = UserUpload.objects.filter(id__in=ids, shop_id=user.shop_id, verify_flag=0).\
                update(verify_flag=verify_flag, accept_flag=accept_flag)
            # notify client
            rejectNotify.pub_message(ids)
            # print connection.queries
            if effectRows == 0:
                return HttpResponse("false")
        return HttpResponse("true")

    def passed(self,request):
        user = request.session['user']

        shopId = user.shop_id
        uploads = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False).order_by('id')[0:pageSize]
        num = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/passed')

    def passed_table(self,request):
        searchText = request.GET['search']
        type = int(request.GET['type'])
        page = int(request.GET['page'])
        user = request.session['user']
        shopId = user.shop_id

        if type == 1:
            uploads = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False, order_id__contains=searchText).order_by('id')[
                      (page - 1) * pageSize:page * pageSize]
            num = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False, order_id__contains=searchText).count()
            pageNum = math.ceil(float(num) / 10)

        elif type == 2:
            uploads = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False, order_id__contains=searchText,refund_flag=1).order_by('id')[
                      (page - 1) * pageSize:page * pageSize]
            num = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False, order_id__contains=searchText,refund_flag=1).count()
            pageNum = math.ceil(float(num) / 10)

        else :
            uploads = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False, order_id__contains=searchText,refund_flag=0).order_by('id')[
                      (page - 1) * pageSize:page * pageSize]
            num = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False, order_id__contains=searchText,refund_flag=0).count()
            pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/passed_table')

    def passed_table_search(self,request):
        text = request.GET['searchText']
        user = request.session['user']

        shopId = user.shop_id
        uploads = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False,order_id__contains=text).order_by('id')[0:pageSize]
        num = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False,order_id__contains=text).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/passed')

    def reject(self,request):
        user = request.session['user']

        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).order_by('id')[
                  0:pageSize]
        num = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/reject')

    def reject_table(self,request):
        user = request.session['user']
        page = int(request.GET['page'])
        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).order_by('id')[
                  (page - 1) * pageSize:page * pageSize]
        num = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/reject_table')
