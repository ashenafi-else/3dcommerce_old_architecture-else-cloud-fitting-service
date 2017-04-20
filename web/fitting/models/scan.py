from django.db import models
from .attachment import Attachment


class Scan(Attachment):
    user = models.ForeignKey('User',)
    scan_id = models.CharField(max_length=256,)
    scanner = models.CharField(max_length=256,)
    scan_type = models.CharField(max_length=100,)
    created_date = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return 'scan_id: {}, user: {}, scanner: {}, type: {}, created_date: {}'.format(
            self.scan_id, self.user_id, self.scanner, self.scan_type, self.created_date)
