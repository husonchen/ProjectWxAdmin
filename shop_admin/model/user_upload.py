from django.db import models

class UserUpload(models.Model):
    class Meta:
        db_table = 'user_upload'
    id = models.IntegerField(primary_key=True)
    shop_id = models.CharField(max_length=255)
    open_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    image1_id = models.CharField(max_length=255)
    image2_id = models.CharField(max_length=255)
    image3_id = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    verify_flag = models.IntegerField()
    accept_flag = models.IntegerField()
    del_flag = models.BooleanField(default=0)