from django.db import models

class Face(models.Model):
	class Meta:
		db_table= "faceid"
	
	idcode = models.CharField(max_length=20)
	img = models.BinaryField()
