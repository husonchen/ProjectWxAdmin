from django_url_framework.controller import ActionController
import xml.etree.ElementTree as ET
from shop_admin.wx.WXBizMsgCrypt import WXBizMsgCrypt
from ProjectWx_admin.settings import APPID,TOKEN,encodingAESKey
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('shop_admin')

class WxController(ActionController):
    @csrf_exempt
    def open(self,request):
        logger.info('wx open')
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        # encrypt_type = request.GET['encrypt_type']
        msg_signature = request.GET['msg_signature']
        data = request.body
        logger.info(data)
        encryp_test = WXBizMsgCrypt(TOKEN, encodingAESKey, APPID)
        ret, encrypt_xml = encryp_test.DecryptMsg(data,msg_signature,timestamp,nonce)

        xml = ET.fromstring(encrypt_xml)
        appid = xml.find('AppId').text
        create_time = xml.find('CreateTime').text
        infotype = xml.find('InfoType').text
        if infotype == 'component_verify_ticket':
            ComponentVerifyTicket = xml.find('ComponentVerifyTicket').text
            print ComponentVerifyTicket


