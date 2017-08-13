from django_url_framework.controller import ActionController
import xml.etree.ElementTree as ET
from shop_admin.wx.WXBizMsgCrypt import WXBizMsgCrypt

class WxController(ActionController):
    def open(self,request):
        data = request.body
        print data
        xml = ET.fromstring(data)
        appid = xml.find('AppId').text
        create_time = xml.find('CreateTime').text
        infotype = xml.find('InfoType').text
        if infotype == 'component_verify_ticket':
            encrt_str = xml.find('ComponentVerifyTicket').text


