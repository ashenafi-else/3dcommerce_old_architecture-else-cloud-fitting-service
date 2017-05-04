from django.db import models


class ModelType(models.Model):

    TYPE_CUSTOM = 'CUSTOM'
    TYPE_FOOT = 'FOOT'
    TYPE_LEFT_FOOT = 'LEFT_FOOT'
    TYPE_RIGHT_FOOT = 'RIGHT_FOOT'

    TYPES = (
        (TYPE_CUSTOM, 'Undefined type'),
        (TYPE_FOOT, 'Foot'),
        (TYPE_LEFT_FOOT, 'Foot left'),
        (TYPE_RIGHT_FOOT, 'Foot right'),
    )

    model_type = models.CharField(
        max_length=64,
        choices=TYPES,
        default=TYPE_CUSTOM,
    )

    class Meta:

        abstract = True
    
    def __str__(self):
        return self.model_type
