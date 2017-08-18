from django_url_framework.controller import ActionController
import xml.etree.ElementTree as ET
from shop_admin.wx.wx_utils import *
import logging
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
        pre_auth_code = get_pre_auth_code()
        return wx_auth_page(pre_auth_code,'/dashboard/')