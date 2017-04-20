from django.db import models


class Product(models.Model):
    uuid = models.CharField(max_length=256)

    def __str__(self):
        return self.uuid
