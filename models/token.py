from django.db import models
from drconf import dr

class Token(models.Model):
	class Meta:
		db_table= "commToken"
	
	tokenId = models.AutoField(primary_key=True , db_column='id')
	platform = models.CharField(max_length=60)
	token = models.CharField(max_length=120)
	fetchTime = models.CharField(max_length=30)
	expires = models.IntegerField()


	def checkExpired(self):
		import datetime
		
		now  = datetime.datetime.now()

		delta = datetime.timedelta(seconds=self.expires)
		fetchT = datetime.datetime.strptime(self.fetchTime , dr.datefmt)

		return ((fetchT + delta) > now)
