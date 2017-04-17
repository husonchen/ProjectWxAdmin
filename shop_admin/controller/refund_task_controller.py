from django_url_framework.controller import ActionController
from shop_admin.util.TplHelper import *
from shop_admin.model.user_upload import UserUpload

class RefundTaskController(ActionController):

    def task(self,request):
        user = request.session['user']
        shopId = user.shop_id
        uploads = UserUpload.objects.filter(shop_id=shopId,del_flag=False).order_by('id')[0:10]

        return getTpl({'uploads':uploads},'translate_task/task')

    def submit(self,request):
        user = request.session['user']
        messageId = request.GET['messageId']
        translateMsg = request.GET['translateMsg']

        effectRows = UserUpload.objects.filter(message_id=messageId,message_translate='').\
                update(message_translate=translateMsg,translator_id=user.translator_id)
        if effectRows == 0:
            return HttpResponse("false")
        else:
            return HttpResponse("true")

    def finished(self,request):
        user = request.session['user']
        messages = UserUpload.objects.filter(translator_id=user.translator_id,del_flag=False).order_by('message_id')[0:10]

        return getTpl({'messages':messages},'translate_task/finished')
