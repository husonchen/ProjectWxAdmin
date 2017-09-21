from django_url_framework.controller import ActionController
import xml.etree.ElementTree as ET
from shop_admin.wx.wx_utils import *
import json
import logging
from shop_admin.model.mp_info import MpInfo
from django.views.decorators.csrf import csrf_exempt
from shop_admin.model.server_config import saveSetting
from shop_admin.nsq_producer.send_message_touser import MessageToUser
from django.http.response import HttpResponse
logger = logging.getLogger('shop_admin')

message_touser = MessageToUser()

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
            if appid == 'wx570bc396a51b8ff8':
                return 'success'
            ComponentVerifyTicket = xml.find('ComponentVerifyTicket').text
            logger.info(ComponentVerifyTicket)
            saveSetting('admin','component_verify_ticket',ComponentVerifyTicket)
        elif infotype == 'unauthorized':
            AuthorizerAppid = xml.find('AuthorizerAppid').text
            logger.info('unauthorized: %s' % AuthorizerAppid)
            MpInfo.objects.filter(authorizer_appid=AuthorizerAppid).update(del_flag=True)
        return 'success'

    def add_mp(self,request):
        user = request.session['user']
        type = request.GET['type']
        pre_auth_code = get_pre_auth_code()
        return wx_auth_page(pre_auth_code,'http://admin.51dingxiao.com/wx/open/shops/%s/%s/' %
                            (type,str(user.shop_id).zfill(5)))

@csrf_exempt
def auto_test(request,appid):  
    if appid != 'wx570bc396a51b8ff8':
        return HttpResponse('')
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    # encrypt_type = request.GET['encrypt_type']
    msg_signature = request.GET['msg_signature']
    data = request.body
    decrypt_xml = get_decrypt_xml(data,msg_signature,timestamp,nonce)
    xml = ET.fromstring(decrypt_xml)
    print decrypt_xml
    if len(data) == 0:
        return HttpResponse('hello, this is handle view')
    else:
        msgType = xml.find('MsgType').text
        reply = None
        toUserName = xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        if msgType == 'event':
	   event = xml.find('Event').text
           content = event + 'from_callback'
	elif msgType == 'text':
	   messageContent = xml.find('Content').text
           if 'QUERY_AUTH_CODE' not in messageContent:
               content = messageContent + '_callback'
           else :
               query_auth_code = messageContent[16:]
               access_token = get_authorizer_access_token(query_auth_code)
               print access_token
               content = query_auth_code + '_from_api'
               message_touser.pub_message({'access_token':access_token,'content':content,'touser':toUserName  })
               #return HttpResponse('') 
        replyWx = '''
                    <xml>
                      <ToUserName><![CDATA[%s]]></ToUserName>
                      <FromUserName><![CDATA[%s]]></FromUserName>
                      <CreateTime>%s</CreateTime>
                      <MsgType><![CDATA[%s]]></MsgType>
                      <Content><![CDATA[%s]]></Content>
                    </xml>
                   '''%(
                        fromUserName,
                        toUserName,
                        createTime,
                        'text',
                        content
                        )                             
        print replyWx
	encrypt_xml = get_encrypt_xml(replyWx,'123476531')
        print encrypt_xml
        return HttpResponse(encrypt_xml)

    

# @csrf_exempt
def redirct_from_wx(request,type,shop_id):
    type = int(type)
    shop_id = int(shop_id)
    authorization_code = request.GET['auth_code']
    logger.info('shop:%d, authorization_code:%s' % (shop_id,authorization_code))

    # MpInfo.objects.update_or_create(shop_id=shop_id,platform=type,
    #                                 defaults={'authorization_code':authorization_code})

    authorizer_appid,authorizer_access_token,authorizer_refresh_token=get_authorizer_access_token(authorization_code)
    MpInfo.objects.update_or_create(
                                    authorizer_appid=authorizer_appid,
                                    defaults={
                                        'shop_id':shop_id,'platform':type,
                                        'authorization_code':authorization_code,
                                        'authorizer_access_token':authorizer_access_token,
                                        'authorizer_refresh_token':authorizer_refresh_token,
                                        'del_flag':False,
                                    })

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
