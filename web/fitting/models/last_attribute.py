from django.db import models


class LastAttribute(models.Model):
    last = models.ForeignKey('Last')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)

    def __str__(self):
        return 'name: {}, value: {}'.format(self.name, self.value)
