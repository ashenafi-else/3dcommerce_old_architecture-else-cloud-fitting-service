from django.db import models


class Scanner(models.Model):
	storage_account = models.ForeignKey('StorageAccount', related_name='scanners')
	scanner_id = models.CharField(max_length=256, unique=True)

	def get_scanner_url(self):
		return f'{self.storage_account.get_account_url()}{self.scanner_id}/'

	def __str__(self):
		return f'scanner_id: {self.scanner_id}'
