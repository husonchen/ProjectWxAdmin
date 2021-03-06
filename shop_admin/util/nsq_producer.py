import requests
from ProjectWx_admin.settings import nsqd
import json

class NsqProducer():
    def __init__(self,topic):
        self.topic = topic
        self.murl = u'http://' + nsqd+'/mpub?topic=' + topic
        self.url = u'http://' + nsqd+'/pub?topic=' + topic


    def produce(self,message):
        m = json.dumps(message)
        requests.post(self.url, data=m)

    def produceList(self,messages):
        payload = [json.dumps(m) for m in messages]
        p = '\n'.join(payload)
        requests.post(self.murl,data=p)