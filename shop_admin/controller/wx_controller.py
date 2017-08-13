from django_url_framework.controller import ActionController
import xml.etree.ElementTree as ET
from shop_admin.wx.WXBizMsgCrypt import WXBizMsgCrypt
from ProjectWx_admin.settings import APPID,TOKEN
import logging

logger = logging.getLogger('shop_admin')

class WxController(ActionController):
    def open(self,request):
        logger.info('wx open')
        # signature = request.GET['signature']
        # timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        # encrypt_type = request.GET['encrypt_type']
        # msg_signature = request.GET['msg_signature']
        data = request.body
        logger.log(data)
        encryp_test = WXBizMsgCrypt(TOKEN, data, APPID)
        ret, encrypt_xml = encryp_test.EncryptMsg(encryp_test, nonce)

        xml = ET.fromstring(encrypt_xml)
        appid = xml.find('AppId').text
        create_time = xml.find('CreateTime').text
        infotype = xml.find('InfoType').text
        if infotype == 'component_verify_ticket':
            ComponentVerifyTicket = xml.find('ComponentVerifyTicket').text
            print ComponentVerifyTicket


