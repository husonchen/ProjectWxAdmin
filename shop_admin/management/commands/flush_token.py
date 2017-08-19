from shop_admin.model.server_config import getSetting,saveSetting
import urllib
import json
import logging
from django.core.management.base import BaseCommand, CommandError
logger = logging.getLogger('shop_admin')
import kronos

@kronos.register('0 * * * *')
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('start flush')
        appId = getSetting('admin','app_id')
        appSecret = getSetting('admin','app_secret')
        component_verify_ticket = getSetting('admin','component_verify_ticket')
        postUrl = ("https://api.weixin.qq.com/cgi-bin/component/api_component_token")
        data = '''{
        "component_appid":"%s" ,
        "component_appsecret": "%s", 
        "component_verify_ticket": "%s" 
        }''' %(appId,appSecret,component_verify_ticket)

        resp = urllib.urlopen(postUrl,data).read()
        urlResp = json.loads(resp)
        logger.info('flush cron: urlResp %s' % urlResp)
        if 'component_access_token' not in urlResp:
            print resp
        accessToken = urlResp['component_access_token']
        saveSetting('admin','component_access_token',accessToken)
