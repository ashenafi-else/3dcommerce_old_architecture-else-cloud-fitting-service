from django.db import models
from web.settings import SCANNER_STORAGE_BASE_URL
# Create your models here.


class User(models.Model):
    uuid = models.CharField(unique=True, max_length=256)
    base_url = models.CharField(max_length=1000, default=SCANNER_STORAGE_BASE_URL)
    sizes = models.ManyToManyField('Size')
    default_scan = models.ForeignKey('Scan', blank=True, null=True, on_delete=models.SET_NULL, related_name='default_scan')

    def __str__(self):
        return 'uuid: {}'.format(self.uuid)