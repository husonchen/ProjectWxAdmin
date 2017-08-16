from django.db import models
from django.core.cache import cache

class ServerConfig(models.Model):
    class Meta:
        db_table = 'admin_config'

    id = models.IntegerField(primary_key=True)
    namespace = models.CharField(max_length=255)
    k = models.CharField(max_length=255)
    v = models.CharField(max_length=255)

def getSetting(namespace,key):
    mc_key = namespace + '_' + key + '_'
    value = cache.get(mc_key)
    if type(value) == type(None):
        try:
            s = ServerConfig.objects.get(namespace=namespace, k=key)
            value = s.v
            cache.set(mc_key,value)
        except:
            return None
    return value

def saveSetting(namespace,key,value):
    mc_key = namespace + '_' + key + '_'
    cache.set(mc_key, value)
    obj, created = ServerConfig.objects.update_or_create(namespace=namespace, k=key,v=value)