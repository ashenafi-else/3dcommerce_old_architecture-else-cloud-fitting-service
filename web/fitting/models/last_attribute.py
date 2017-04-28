from django.db import models
from .attribute import Attribute


class LastAttribute(Attribute):
    last = models.ForeignKey('Last')
    left_limit_value = models.FloatField(null=False, default=0)
    best_value = models.FloatField(null=False, default=0)
    right_limit_value = models.FloatField(null=False, default=0)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        
        return super().__str__() + f', disabled: {self.disabled}'

