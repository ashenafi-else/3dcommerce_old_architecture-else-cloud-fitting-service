from django.db import models

class Attribute(models.Model):

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)

    def __str__(self):
        return 'name: {}, value: {}'.format(self.name, self.value)

    class Meta:

        abstract = True
