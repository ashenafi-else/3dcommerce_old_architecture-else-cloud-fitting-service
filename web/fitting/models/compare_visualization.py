from django.db import models
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

import os


class CompareVisualization(models.Model):

	last = models.ForeignKey('Last', null=True,)
	scan_1 = models.ForeignKey('Scan', related_name='scan_1', null=False,)
	scan_2 = models.ForeignKey('Scan', related_name='scan_2', null=True, blank=True)
	output_model = models.CharField(max_length=1000, blank=True)
	output_model_3d = models.CharField(max_length=1000, blank=True)

	class Meta:

		unique_together = (('last', 'scan_1', 'scan_2'),)

	def __str__(self):
		return f'last: {self.last}, scan_1: {self.scan_1}, scan_2: {self.scan_2}, result: {self.output_model_3d}'

@receiver(models.signals.post_delete, sender=CompareResult)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.output_model:
        if os.path.isfile(instance.output_model):
            os.remove(instance.output_model)
        if os.path.isfile(instance.output_model_3d):
            os.remove(instance.output_model_3d)
