from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from shop_admin.model.user_upload import UserUpload
from shop_admin.model.verify_refund import VerifyRefund
from shop_admin.model.log_change_money import LogShopMoney
import math

class RefundTaskController(ActionController):

    def task(self,request):
        user = request.session['user']
        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId,del_flag=False,verify_flag=0).order_by('id')[0:10]
        num = UserUpload.objects.filter(shop_id=shopId,del_flag=False,verify_flag=0).count()
        pageNum = math.ceil(float(num)/10)
        return getTpl({'uploads':uploads,'pageNum':pageNum},'refund_task/task')


    def task_table(self,request):
        page = int(request.GET['page'])
        user = request.session['user']
        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId,del_flag=False).order_by('id')[(page-1)*10:page*10]

        return getTpl({'uploads':uploads},'refund_task/task_table')

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

        effectRows = UserUpload.objects.filter(id=id,shop_id=user.shop_id,verify_flag=0).\
                update(verify_flag=verify_flag,accept_flag=accept_flag)

        if effectRows == 0:
            return HttpResponse("false")
        else:
            upload = UserUpload.objects.filter(id=id)[0]
            logMoney = LogShopMoney.objects.filter(shop_id=user.shop_id).order_by('-id')[0]
            v = VerifyRefund(shop_id=user.shop_id,open_id=upload.open_id,order_id=upload.order_id,
                         money=logMoney.money,update_time=None,create_time=None)
            v.save()
            return HttpResponse("true")

    def passed(self,request):
        user = request.session['user']

        shopId = user.shop_id
        uploads = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False).order_by('id')[0:10]
        num = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/passed')

    def passed_table(self,request):
        page = int(request.GET['page'])
        user = request.session['user']
        shopId = user.shop_id
        uploads = VerifyRefund.objects.filter(shop_id=shopId, del_flag=False).order_by('id')[(page - 1) * 10:page * 10]

        return getTpl({'uploads': uploads}, 'refund_task/passed_table')

    def reject(self,request):
        user = request.session['user']

        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).order_by('id')[
                  0:10]
        num = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/reject')

    def reject_table(self,request):
        user = request.session['user']

        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).order_by('id')[
                  0:10]
        num = UserUpload.objects.filter(shop_id=shopId, del_flag=False, verify_flag=2).count()
        pageNum = math.ceil(float(num) / 10)
        return getTpl({'uploads': uploads, 'pageNum': pageNum}, 'refund_task/reject_table')
