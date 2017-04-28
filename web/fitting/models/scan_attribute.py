from django.db import models
from .attribute import Attribute


class ScanAttribute(Attribute):
    user = models.ForeignKey('User')
    scan = models.ForeignKey('Scan')

