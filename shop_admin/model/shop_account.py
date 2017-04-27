from django.db import models

class ShopAccount(models.Model):
    class Meta:
        db_table = 'shop_account'

    shop_id = models.IntegerField(primary_key=True)
    balance = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    del_flag = models.BooleanField(default=0)