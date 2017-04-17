from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from django.http import  HttpResponseRedirect

class DashboardController(ActionController):

    def index(self,request):
        # if request.session.has_key('user') is False:
        #     return HttpResponseRedirect('/login/')
        user = request.session['user']
        c = {"userName":user.shop_name}
        return getTpl(c,'dashboard/index')