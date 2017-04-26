from django.db import models
from django.dispatch import receiver
from datetime import datetime
from ..utils import gen_file_name
import os


class Attachment(models.Model):

	attachment = models.FileField(upload_to=gen_file_name)

	class Meta:
		
		abstract = True
