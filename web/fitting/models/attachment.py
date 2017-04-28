from django.db import models
from ..utils import gen_file_name


class Attachment(models.Model):

	attachment = models.FileField(upload_to=gen_file_name)

	class Meta:
		
		abstract = True
