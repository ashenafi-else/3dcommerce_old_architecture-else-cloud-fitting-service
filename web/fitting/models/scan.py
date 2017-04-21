from django.db import models
from .attachment import Attachment
from django.dispatch import receiver

import os


class Scan(Attachment):
	user = models.ForeignKey('User',)
	scan_id = models.CharField(max_length=256,)
	scanner = models.CharField(max_length=256,)
	scan_type = models.CharField(max_length=100,)
	created_date = models.DateTimeField(auto_now=True,)

	def __str__(self):
		return 'scan_id: {}, user: {}, scanner: {}, type: {}, created_date: {}'.format(
			self.scan_id, self.user_id, self.scanner, self.scan_type, self.created_date)


@receiver(models.signals.post_delete, sender=Scan)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)


