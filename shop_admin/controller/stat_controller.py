from django_url_framework.controller import ActionController
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Sum
from shop_admin.model.verify_refund import VerifyRefund
from shop_admin.model.shop_stats import ShopStats
import json
import datetime

class StatController(ActionController):
    def refund(self,request):
        user = request.session['user']
        shop_id = user.shop_id
        today = datetime.date.today()
        tomonth = int(today.replace(day=1).strftime('%Y%m%d'))
        rf = VerifyRefund.objects.all().filter(create_time__gte = today,shop_id=shop_id).values('shop_id').annotate(refund_num=Count('id'),refund_money=Sum('money')).all()
        if len(rf) == 0:
            rf = {}
            rf['refund_num'] = 0
            rf['refund_money'] = 0
        else:
            rf = rf[0]
        shopstats = ShopStats.objects.filter(shop_id=shop_id).order_by('-day')[0:10]
        try:
            mstats = ShopStats.objects.all().filter(day__gte = tomonth,shop_id=shop_id).values('shop_id').annotate(m_refund_num=Sum('refund_num'),m_refund_money=Sum('refund_money'))[0]
        except:
            mstats = {'m_refund_num':0,'m_refund_money':0}
        num_data = []
        money_data = []
        date_data = []
        for shopstat in reversed(shopstats):
            num_data.append(shopstat.refund_num)
            money_data.append(float(shopstat.refund_money)/100)
            date_data.append(shopstat.day)
        c = {'refund_num':rf['refund_num'],'refund_money':float(rf['refund_money']) / 100,
             'num_data':json.dumps(num_data),'money_data':json.dumps(money_data),'date_data':json.dumps(date_data),
             'm_refund_num':mstats['m_refund_num']+rf['refund_num'],'m_refund_money':float(mstats['m_refund_money']+rf['refund_money'])/100}
        return render(request, 'stat/refund.html', c)