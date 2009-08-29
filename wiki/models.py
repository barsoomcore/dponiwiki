from django.db import models

# Create your models here.
class Page(models.Model):
	name = models.CharField(max_length="20", primary_key=True)
	content = models.TextField(blank=True)

