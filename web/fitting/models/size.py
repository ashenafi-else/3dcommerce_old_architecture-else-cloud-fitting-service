from django.db import models


class Size(models.Model):

    TYPE_CUSTOM = 'CUSTOM'
    TYPE_SHOESIZE = 'SHOESIZE'

    TYPES = (
        (TYPE_CUSTOM, 'Undefined type'),
        (TYPE_SHOESIZE, 'Shoe size'),
    )

    size_type = models.CharField(
        max_length=64,
        choices=TYPES,
        default=TYPE_CUSTOM,
    )

    value = models.CharField(max_length=64)
    numeric_value = models.IntegerField()
    
    def __str__(self):
        return '{} - {}'.format(self.size_type, self.value)
