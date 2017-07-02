#this file is used for shop statist
import MySQLdb as mdb
import sys
import urllib
import json
import os
import datetime

reload(sys)
exec("sys.setdefaultencoding('utf-8')")

today=datetime.date.today()
oneday=datetime.timedelta(days=1)
yesterday=(today-oneday)
yesterday_int = int(yesterday.strftime('%Y%m%d'))
yesterday_s = yesterday.strftime('%Y-%m-%d')
today_s = today.strftime('%Y-%m-%d')

con = mdb.connect('127.0.0.1', 'xiaob', 'skdfjkasdf', 'xiaob')
con.set_character_set('utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
con.commit()

cur.execute("SELECT DISTINCT (shop_id) from shop_setting")
shops = cur.fetchall()
print yesterday_s
print today_s
cur.execute('SELECT shop_id,count(1),sum(money) from verify_refund where create_time>=%s and create_time<%s group by shop_id ',(yesterday_s,today_s))
refunds = cur.fetchall()
refundDict = {}
for refund in refunds:
    refundDict[refund[0]] = refund
for shop in shops:
    shop_id = shop[0]
    if shop_id not in refundDict:
        cur.execute("Insert into shop_stats(shop_id,day,refund_num,refund_money) values(%d,%d,%d,%d)"
                    % (shop_id,yesterday_int,0,0))
    else:
	refund = refundDict[shop_id]
        cur.execute("Insert into shop_stats(shop_id,day,refund_num,refund_money) values(%d,%d,%d,%d)"
                    % (shop_id, yesterday_int, refund[1], refund[2]))

    con.commit()
