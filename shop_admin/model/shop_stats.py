from django.db import models

class ShopStats(models.Model):
    class Meta:
        db_table = 'shop_stats'
    id = models.IntegerField(primary_key=True)
    shop_id = models.IntegerField()
    day = models.IntegerField()
    refund_num = models.IntegerField()
    refund_money = models.IntegerField()

