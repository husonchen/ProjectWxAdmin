import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from shop_admin.model.server_config import getSetting,saveSetting
import urllib
import json

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
if 'component_access_token' not in urlResp:
    print resp
accessToken = urlResp['component_access_token']
saveSetting('admin','component_access_token',accessToken)
