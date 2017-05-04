from django.db import models
from .model_type import ModelType


class Size(ModelType):

    value = models.CharField(max_length=64)
    numeric_value = models.IntegerField()

    class Meta:

        unique_together = (('model_type', 'value',),)
    
    def __str__(self):
        return '{} - {}'.format(str(self.model_type), self.value)
