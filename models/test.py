from django.db import models

class Test(models.Model):
	class Meta:
		db_table= "test"
	
	a = models.IntegerField()
	b = models.IntegerField()
