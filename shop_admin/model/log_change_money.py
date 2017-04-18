from django.db import models

class LogShopMoney(models.Model):
    class Meta:
        db_table = 'log_change_money'

    id = models.IntegerField(primary_key=True)
    shop_id = models.CharField(max_length=255)
    money = models.FloatField()
    create_time = models.DateTimeField()
