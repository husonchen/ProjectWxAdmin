from django.db import models

class ShopUser(models.Model):
    class Meta:
        db_table = 'shop_user'
    shop_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    del_flag = models.BooleanField(default=0)
