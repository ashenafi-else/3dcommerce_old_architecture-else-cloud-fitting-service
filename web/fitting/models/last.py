from django.db import models
from .attachment import Attachment


class Last(Attachment):
    size = models.ForeignKey('Size',)
    product = models.ForeignKey('Product',)

    def __str__(self):
        return 'product: {}, size: {}'.format(str(self.product), str(self.size))
