from django.db import models
from django.dispatch import receiver
import os


def gen_file_name(instance, filename):
	if instance.__class__.__name__ == 'Last':
		uuid = instance.product.uuid
		date_or_size = instance.size
	else:
		uuid = instance.user.uuid
		date_or_size = instance.created_date
	return os.path.sep.join([instance.__class__.__name__, uuid, str(date_or_size), filename])


class Attachment(models.Model):

	attachment = models.FileField(upload_to=gen_file_name)

	class Meta:
		
		abstract = True


@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print(instance.attachment)
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)

