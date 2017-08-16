from shop_admin.wx.WXBizMsgCrypt import WXBizMsgCrypt
from shop_admin.model.server_config import getSetting
from ProjectWx_admin.settings import TOKEN

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