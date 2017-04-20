from django.db import models


class Attribute(models.Model):
    user = models.ForeignKey('User')
    scan = models.ForeignKey('Scan')
    name = models.CharField(max_length=100)
    value_for_left = models.CharField(max_length=1000)
    value_for_right = models.CharField(max_length=1000)

    def __str__(self):
        return 'user: {}, scan: {}, name: {}'.format(self.user, self.scan.scan_id, self.name)
