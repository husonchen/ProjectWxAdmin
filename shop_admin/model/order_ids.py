from django.db import models

class OrderIds(models.Model):
    class Meta:
        db_table = 'order_ids'

    shop_id = models.IntegerField(primary_key=True)
    order_id = models.CharField(max_length=255)
    create_time = models.DateTimeField()