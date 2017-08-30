from shop_admin.wx.WXBizMsgCrypt import WXBizMsgCrypt
from shop_admin.model.server_config import getSetting,ServerConfig
from ProjectWx_admin.settings import TOKEN
from shop_admin.model.mp_info import MpInfo
import urllib3
import warnings
warnings.filterwarnings("ignore")
import json
http = urllib3.PoolManager()
import logging
logger = logging.getLogger('shop_admin')
from django.http import HttpResponseRedirect

def get_encrypt_xml(reply_xml, nonce):
    APPID = getSetting('admin', 'app_id')
    encodingAESKey = getSetting('admin', 'encodingAESKey')
    encrypt = WXBizMsgCrypt(TOKEN, encodingAESKey, APPID)
    ret_encrypt, encrypt_xml = encrypt.EncryptMsg(reply_xml, nonce)
    if ret_encrypt == 0:
        return encrypt_xml
    else:
        return ''

def get_decrypt_xml(encrypt_xml, msg_signature, timestamp, nonce):
    APPID = getSetting('admin','app_id')
    encodingAESKey = getSetting('admin','encodingAESKey')
    if 'ToUserName' not in encrypt_xml:
        encrypt_xml = encrypt_xml.replace('AppId','ToUserName')
    decrypt = WXBizMsgCrypt(TOKEN, encodingAESKey, APPID)
    ret_decrypt, decrypt_xml = decrypt.DecryptMsg(encrypt_xml,
                                         msg_signature,
                                         timestamp,
                                         nonce)
    if ret_decrypt == 0:
        return decrypt_xml
    else:
        return ''

def get_pre_auth_code():
    component_access_token = getSetting('admin','component_access_token')
    appid = getSetting('admin','app_id')
    target = r'https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token=%s' %component_access_token
    data = {'component_appid':appid}
    payload = json.dumps(data)
    s = http.request('POST',target,body=payload)
    res = json.loads(s.data)
    if 'pre_auth_code' not in res:
        logger.error('get_pre_auth_code return : %s' % s.data)
    return res['pre_auth_code']

# def get_pre_authorization_code():
#     component_access_token = getSetting('admin', 'component_access_token')
#     appid = getSetting('admin', 'app_id')
#     target = r'https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token=%s' % component_access_token
#     data = {'component_appid': appid}
#     payload = json.dumps(data)
#     s = http.request('POST', target, body=payload)
#     res = json.loads(s.data)
#     if 'pre_auth_code' not in res:
#         logger.error('get_pre_auth_code return : %s' % s.data)
#     return res['pre_auth_code']

def wx_auth_page(pre_auth_code,redirect_uri):
    appid = getSetting('admin', 'app_id')
    url = 'https://mp.weixin.qq.com/cgi-bin/componentloginpage?component_appid=%s&pre_auth_code=%s' \
          '&redirect_uri=%s' %(appid,pre_auth_code,redirect_uri)
    return HttpResponseRedirect(url)


def get_authorizer_access_token(authorization_code):
    component_access_token = getSetting('admin', 'component_access_token')
    appid = getSetting('admin', 'app_id')
    target = r'https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token=%s' % component_access_token
    data = {'component_appid': appid,
            'authorization_code': authorization_code}
    payload = json.dumps(data)
    s = http.request('POST', target, body=payload)
    res = json.loads(s.data)
    if 'authorization_info' not in res:
        logger.error('get_authorizer_access_token return : %s' % s.data)
    res=res['authorization_info']
    return res['authorizer_appid'],res['authorizer_access_token'],res['authorizer_refresh_token']


def flush_authorization_token(authorizer_appid,authorizer_refresh_token):
    component_access_token = getSetting('admin', 'component_access_token')
    appid = getSetting('admin', 'app_id')
    target = r'https://api.weixin.qq.com/cgi-bin/component/api_authorizer_token?component_access_token=%s' % component_access_token
    data = {'component_appid': appid,'authorizer_appid':authorizer_appid,'authorizer_refresh_token':authorizer_refresh_token}
    payload = json.dumps(data)
    s = http.request('POST', target, body=payload)
    res = json.loads(s.data)
    if 'authorizer_access_token' not in res:
        logger.error('flush_authorization_token return : %s' % s.data)
    return res['authorizer_access_token'],res['authorizer_refresh_token']

def get_basic_info(auth_appid_value):
    component_access_token = getSetting('admin', 'component_access_token')
    appid = getSetting('admin', 'app_id')
    target = r'https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_info?component_access_token=%s' % component_access_token
    data = {'component_appid': appid, 'authorizer_appid': auth_appid_value}
    payload = json.dumps(data)
    s = http.request('POST', target, body=payload)
    res = json.loads(s.data)
    if 'authorizer_info' not in res:
        logger.error('get_basic_info return : %s' % s.data)
    res = res['authorizer_info']
    return res

def createTag(name,id):
    accessToken = MpInfo.objects.filter(id=id).all()[0].authorizer_access_token
    target = r'https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s' %accessToken
    data = {'tag':{'name':name}}
    payload = json.dumps(data)
    s = http.request('POST',target,body=payload)
    res = json.loads(s.data)
    return res['tag']['id']