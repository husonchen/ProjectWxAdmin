#this file is used for download QR Code
import MySQLdb as mdb
import sys
import urllib
import json
import os

targetDir = os.path.join(sys.path[0],'static/qrcode')
reload(sys)
exec("sys.setdefaultencoding('utf-8')")

con = mdb.connect('localhost', 'xiaob', 'skdfjkasdf', 'xiaob')
con.set_character_set('utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
con.commit()


class QRCode():
    """docstring for """
    def __init__(self):
        pass

    def GET_QR(self,accessToken,scene_id):
        postData = """{
        "action_name":"QR_LIMIT_SCENE",
        "action_info": {"scene": {"scene_id": %d }}
        }""" %scene_id
        postUrl = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)

        xml_str = urlResp.read()
        json_str = json.loads(xml_str)
        ticket = json_str["ticket"]
#        urlencode(ticket)
        QRcodeUrl = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" %ticket
        urllib.urlretrieve(QRcodeUrl, "%s/%s.jpg" % (targetDir, scene_id))
	print 'save image at %s/%s.jpg' % (targetDir, scene_id)


scene_id = int(raw_input('scene_id: '))
cur.execute("SELECT v from server_config where k = 'access_token' and name_space='wx'")
data = cur.fetchone()
accessToken = data[0]
xwpayQR= QRCode()
xwpayQR.GET_QR(accessToken,scene_id)
    
