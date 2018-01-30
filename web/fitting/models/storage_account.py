from django.db import models
from django.conf import settings


class StorageAccount(models.Model):

	login = models.CharField(max_length=256, default=settings.DEFAULT_STORAGE_LOGIN)
	password = models.CharField(max_length=256, default=settings.DEFAULT_STORAGE_PASSWORD)
	access = models.CharField(max_length=256, default=settings.DEFAULT_STORAGE_ACCOUNT_ACCESS)

	def get_account_url(self):
		return f'https://{self.login}:{self.password}@avatar3d.ibv.org:8443/{self.access}/{self.login.upper()}/'

	def __str__(self):
		return f'login: {self.login}, access: {self.access}'
