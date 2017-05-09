from django.db import models
from django.db import connection

class OrderIds(models.Model):
    class Meta:
        db_table = 'order_ids'

    shop_id = models.IntegerField(primary_key=True)
    order_id = models.CharField(max_length=255)
    create_time = models.DateTimeField()

    def batchInsert(self,id_list,shop_id):
        pairList = []
        for id in id_list:
            pairList.append((id,shop_id))
        placeHolders = ",".join("(%s, %s, null)" for _ in pairList)
        sql = "INSERT IGNORE order_ids(order_id,shop_id,create_time) values %s" % placeHolders
        flattened_values = [item for sublist in pairList for item in sublist]
        with connection.cursor() as cursor:
            cursor.execute(sql,flattened_values)
