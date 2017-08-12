#this file is used for admin charge user money
import MySQLdb as mdb
shop_id = int(raw_input('shop_id: '))
#yuan
money = int(raw_input('money(yuan): '))
con = mdb.connect('localhost', 'xiaob', 'skdfjkasdf', 'xunhui')
cur = con.cursor()
money = money * 100
cur.execute('Insert into charge_history(shop_id, amount, create_time) VALUES (%d,%d,null)'%(shop_id,money))
cur.execute('Update shop_account set balance=balance+%d where shop_id=%d'%(money,shop_id))
con.commit()
con.close()
