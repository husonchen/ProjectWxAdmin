from django.db import models

class MpInfo(models.Model):
    class Meta:
        db_table = 'mp_info'

    id = models.IntegerField(primary_key=True)
    authorization_code = models.CharField(max_length=255)
    authorizer_access_token = models.CharField(max_length=255)
    authorizer_appid = models.CharField(max_length=255)
    authorizer_refresh_token = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    head_img = models.CharField(max_length=255)
    service_type_info = models.IntegerField(default=0)
    verify_type_info = models.IntegerField(default=0)
    user_name = models.CharField(max_length=255)
    principal_name = models.CharField(max_length=255)
    qrcode_url = models.CharField(max_length=255)
    shop_id = models.IntegerField(default=0)
    platform = models.IntegerField(default=0)
    del_flag = models.BooleanField(default=0)