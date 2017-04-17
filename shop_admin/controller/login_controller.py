from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from shop_admin.model.shop_user import ShopUser

class LoginController(ActionController):

    def hello(self,request):
        print("hello")
        for user in ShopUser.objects.all():
            print user
        return getTpl({},'login/hello')

    def index(self,request):
        return getTpl({},'login/login')

    def login(self,request):
        password = request.GET['password']
        username = request.GET['username']
        try :
            user = ShopUser.objects.get(user_name=username, password=password, del_flag=False)
        except :
            return HttpResponse("false");

        request.session['user'] = user
        return HttpResponse("true")

    def register(self,request):
        username = request.GET['username']
        password = request.GET['password']
        email = request.GET['email']
        translator = ShopUser(user_name=username, user_password=password, mail_address=email)
        translator.save()
        return HttpResponse("true")
