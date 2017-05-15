from django.db import models
from .attribute import Attribute


class ScanAttribute(Attribute):
    scan = models.ForeignKey('Scan')

