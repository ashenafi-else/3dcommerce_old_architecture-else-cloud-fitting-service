from django.db import models
from django.dispatch import receiver
import os


class CompareResult(models.Model):

	MIN = 0
	MAX = 100

	TYPE_SCAN = 'SCAN'
	TYPE_FITTING = 'FITTING'

	TYPES = (
		(TYPE_SCAN, 'scan'),
		(TYPE_FITTING, 'fitting'),
	)

	MODE_3D = '3D'
	MODE_METRICS = 'METRICS'

	MODES = (
		(MODE_3D, '3d'),
		(MODE_METRICS, 'metrics'),
	)

	last = models.ForeignKey('Last', null=True,)
	scan_1 = models.ForeignKey('Scan', related_name='scan_1', null=False,)
	scan_2 = models.ForeignKey('Scan', related_name='scan_2', null=True, blank=True)
	compare_result = models.FloatField()
	output_model = models.CharField(max_length=1000, blank=True)
	compare_type = models.CharField(
		max_length=64,
		choices=TYPES,
		default=TYPE_FITTING,
	)
	compare_mode = models.CharField(
		max_length=64,
		choices=MODES,
		default=MODE_3D,
	)

	class Meta:

		unique_together = (('last', 'scan_1', 'scan_2'),)

	def __str__(self):
		return f'last: {self.last}, scan_1: {self.scan_1}, scan_2: {self.scan_2}, result: {self.compare_result}'

@receiver(models.signals.post_delete, sender=CompareResult)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.output_model:
        if os.path.isfile(instance.output_model):
            os.remove(instance.output_model)
