from django.db import models
from .attachment import Attachment
from django.dispatch import receiver

import os


class Last(Attachment):
    size = models.ForeignKey('Size',)
    product = models.ForeignKey('Product',)

    def __str__(self):
        return 'product: {}, size: {}'.format(str(self.product), str(self.size))


@receiver(models.signals.post_delete, sender=Last)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)

