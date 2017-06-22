from django.db import models
from .attachment import Attachment
from django.dispatch import receiver


class Product(Attachment):
    uuid = models.CharField(max_length=256)

    def __str__(self):
        return self.uuid


@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)

