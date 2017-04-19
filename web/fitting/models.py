from django.db import models
from web.settings import SCANNER_STORAGE_BASE_URL
# Create your models here.


class Scan(models.Model):
    scan_id = models.CharField(max_length=256)
    user_id = models.IntegerField()

    original_left_foot_path = models.CharField(max_length=1000)
    original_right_foot_path = models.CharField(max_length=1000)

    path_left_foot_in_fitting_service = models.CharField(max_length=1000)
    path_right_foot_in_fitting_service = models.CharField(max_length=1000)

    scanner = models.CharField(max_length=256)
    type = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id: {}, scan_id: {}, user_id: {}, scanner: {}, type: {}'.format(
            self.id, self.scan_id, self.user_id, self.scanner, self.type)


class Shoe(models.Model):
    uuid = models.CharField(max_length=256)
    size = models.IntegerField()
    path = models.CharField(max_length=1000)
    path_in_fitting_service = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.uuid, self.size)


class Sizes(models.Model):

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

    def __str__(self):
        return '{} - {}' % self.size_type, self.value


class Last(models.Model):
    size = models.CharField(max_length=64)
    attachment = models.FileField()
    path = models.CharField(max_length=1000, blank=True)
    product = models.ForeignKey(
        'Product'
    )

    def __str__(self):
        return self.size


class Product(models.Model):
    uuid = models.CharField(max_length=256)

    def __str__(self):
        return self.uuid


class User(models.Model):
    uuid = models.CharField(unique=True, max_length=256)
    base_url = models.CharField(max_length=1000, default=SCANNER_STORAGE_BASE_URL)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    default_scan_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'id: {}, uuid: {}'.format(self.id, self.uuid)


class Attribute(models.Model):
    user_id = models.IntegerField()
    scan_id = models.IntegerField()
    name = models.CharField(max_length=100)
    value_for_left = models.CharField(max_length=1000)
    value_for_right = models.CharField(max_length=1000)

    def __str__(self):
        return 'user_id: {}, scan_id: {}, name: {}'.format(self.user_id, self.scan_id, self.name)


class CompareResults(models.Model):

    shoe_id = models.IntegerField()
    scan_id = models.IntegerField()
    compare_result = models.FloatField()
    output_model = models.CharField(max_length=1000)

    class Meta:

        unique_together = (('shoe_id', 'scan_id'),)

    def __str__(self):
        return 'shoe_id: {}, scan_id: {}, result: {}'.format(self.shoe_id, self.scan_id, self.compare_result)
