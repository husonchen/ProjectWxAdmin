from shop_admin.model.server_config import getSetting,saveSetting
import urllib
import json
import logging
from django.core.management.base import BaseCommand, CommandError
from shop_admin.wx.wx_utils import *
from shop_admin.model.mp_info import MpInfo
logger = logging.getLogger('shop_admin')
import kronos
from django.core.cache import cache
import pylibmc as mc

@kronos.register('0 * * * *')
class Command(BaseCommand):
    def handle(self, *args, **options):
        client = mc.Client(['127.0.0.1:11211'])
        qs = MpInfo.objects.all()
        # print qs
        for q in qs:
            try:
                authorizer_access_token,authorizer_refresh_token = flush_authorization_token(q.authorizer_appid,q.authorizer_refresh_token)
                info = get_basic_info(q.authorizer_appid)
                # print info
                if 'head_img' not in info:
                    info['head_img'] = '/assets/img/default_head.jpeg'
                MpInfo.objects.filter(authorizer_appid=q.authorizer_appid).update(
                    authorizer_access_token=authorizer_access_token,
                    authorizer_refresh_token=authorizer_refresh_token,

                    nick_name = info['nick_name'],
                    head_img = info['head_img'],
                    service_type_info = info['service_type_info']['id'],
                    verify_type_info = info['verify_type_info']['id'],
                    user_name = info['user_name'],
                    principal_name = info['principal_name'],
                    qrcode_url = info['qrcode_url'],
                )

                mpinfo = MpInfo.objects.filter(authorizer_appid=q.authorizer_appid).all()[0]
                client.delete('xunhui__mp_info_id_%d'%mpinfo.id)
                client.delete('xunhui__mp_info_appid_'+q.authorizer_appid)
            except:
                continue
