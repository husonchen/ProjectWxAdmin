from django.db import models

class ShopSetting(models.Model):
    class Meta:
        db_table = 'shop_setting'
    shop_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    namespace = models.CharField(max_length=255)
    update_time = models.DateTimeField()
    filter_orderid_flag = models.BooleanField(default=False)
    auto_pass_flag = models.BooleanField(default=False)
