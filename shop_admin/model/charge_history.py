from django.db import models

class ChargeHistory(models.Model):
    class Meta:
        db_table = 'charge_history'

    id = models.IntegerField(primary_key=True)
    shop_id = models.IntegerField()
    amount = models.IntegerField()
    create_time = models.DateTimeField()