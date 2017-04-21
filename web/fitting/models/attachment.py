from django.db import models
from django.dispatch import receiver
from datetime import datetime
import os


def gen_file_name(instance, filename):
	if instance.__class__.__name__ == 'Last':
		uuid = instance.product.uuid
		date_or_size = instance.size
	else:
		uuid = instance.user.uuid
		now = datetime.now()
		date_or_size = '{}-{}-{}'.format(now.year, now.month, now.day)
	return os.path.sep.join([instance.__class__.__name__, uuid, str(date_or_size), filename])


class Attachment(models.Model):

	attachment = models.FileField(upload_to=gen_file_name)

	class Meta:
		
		abstract = True
