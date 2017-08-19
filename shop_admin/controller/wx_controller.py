from django_url_framework.controller import ActionController
import xml.etree.ElementTree as ET
from shop_admin.wx.wx_utils import *
import logging
from shop_admin.model.mp_info import MpInfo
from django.views.decorators.csrf import csrf_exempt
from shop_admin.model.server_config import saveSetting
logger = logging.getLogger('shop_admin')

class WxController(ActionController):
    @csrf_exempt
    def open(self,request):
        logger.info('wx open')
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        # encrypt_type = request.GET['encrypt_type']
        msg_signature = request.GET['msg_signature']
        data = request.body

        decrypt_xml = get_decrypt_xml(data,msg_signature,timestamp,nonce)
        xml = ET.fromstring(decrypt_xml)
        appid = xml.find('AppId').text
        create_time = xml.find('CreateTime').text
        infotype = xml.find('InfoType').text
        if infotype == 'component_verify_ticket':
            ComponentVerifyTicket = xml.find('ComponentVerifyTicket').text
            logger.info(ComponentVerifyTicket)
            saveSetting('admin','component_verify_ticket',ComponentVerifyTicket)
        return 'success'

    def add_mp(self,request):
        user = request.session['user']
        type = request.GET['type']
        pre_auth_code = get_pre_auth_code()
        return wx_auth_page(pre_auth_code,'http://admin.51dingxiao.com/wx/open/shops/%s/%s/' %
                            (type,str(user.shop_id).zfill(5)))

# @csrf_exempt
def redirct_from_wx(request,type,shop_id):
    type = int(type)
    shop_id = int(shop_id)
    authorization_code = request.GET['auth_code']
    logger.info('shop:%d, authorization_code:%s' % (shop_id,authorization_code))

    # MpInfo.objects.update_or_create(shop_id=shop_id,platform=type,
    #                                 defaults={'authorization_code':authorization_code})

    authorizer_appid,authorizer_access_token,authorizer_refresh_token=get_authorizer_access_token(authorization_code)
    MpInfo.objects.update_or_create(shop_id=shop_id,platform=type,
                                    authorization_code=authorization_code,
                                    authorizer_access_token=authorizer_access_token,
                                    authorizer_refresh_token=authorizer_refresh_token,
                                    defaults={'authorizer_appid':authorizer_appid})

    info = get_basic_info(authorizer_appid)
    if 'head_img' not in info:
        info['head_img'] = '/assets/img/default_head.jpeg'
    # print info
    MpInfo.objects.filter(authorizer_appid=authorizer_appid).update(
        authorizer_access_token=authorizer_access_token,
        authorizer_refresh_token=authorizer_refresh_token,

        nick_name=info['nick_name'],
        head_img=info['head_img'],
        service_type_info=info['service_type_info']['id'],
        verify_type_info=info['verify_type_info']['id'],
        user_name=info['user_name'],
        principal_name=info['principal_name'],
        qrcode_url=info['qrcode_url'],
    )

    return HttpResponseRedirect('/dashboard/')