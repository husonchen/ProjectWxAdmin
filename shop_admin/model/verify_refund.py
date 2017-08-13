from django.db import models

class VerifyRefund(models.Model):
    class Meta:
        db_table = 'verify_refund'
    id = models.IntegerField(primary_key=True)
    shop_id = models.CharField(max_length=255)
    open_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    refund_flag = models.BooleanField(default=0)
    money = models.FloatField()
    del_flag = models.BooleanField(default=0)

    # def save(self, *args, **kwargs):
    #     if not self.create_time:
    #         self.create_time = None
    #     super(VerifyRefund,self).save(*args, **kwargs)