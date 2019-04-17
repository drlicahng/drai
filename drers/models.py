# -*- encoding:utf-8 -*-
from django.db import models
import logging
from drconf import dr
log = logging.getLogger(dr.TAG)

 

class MaintenancePerson(models.Model):
	class Meta:
		abstract = True
	
	@classmethod
	def new(Class, tableName):
		class Meta:
			db_table = tableName

		attrs = {
			'__module__':Class.__module__,		
			'Meta':Meta
		}
	
		return type(tableName , (Class,),attrs)


	pid = models.AutoField(primary_key=True , db_column='id')
	name = models.CharField(max_length=32)
	idno = models.CharField(max_length=32)
	mobile = models.CharField(max_length=32)
	wechat = models.CharField(max_length=32)
	img = models.CharField(max_length=64)
	content = models.CharField(max_length=255)
	openid = models.CharField(max_length=32)
	status = models.CharField(max_length=2)
	facilitatorId = models.CharField(max_length=32)





class BankCodeTable(models.Model):
	class Meta:
		db_table = 'bankcodetable'
	

	bid = models.AutoField(primary_key=True , db_column='id')
	bankCode = models.CharField(max_length=10)
	tableName = models.CharField(max_length=50)
	mark = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	content = models.CharField(max_length=100)



class Terminal(models.Model):
	class Meta:
		db_table = 'departterminal'
	

	tid = models.AutoField(primary_key=True , db_column='id')
	departId = models.IntegerField()
	terminalId = models.CharField(max_length=40)
	content = models.CharField(max_length=100)
	mac = models.CharField(max_length=40)
	bankCode = models.CharField(max_length=10)
	bigVer = models.IntegerField()
	shortVer = models.IntegerField()
	departTreeId = models.CharField(max_length=255)
	lastAccessTime = models.CharField(max_length=30)

'''

table 's service function
1.

'''



#update
def queryEngineerNameByIdno(terminalId , idcode):
	try:
		log.debug('[DBQUERY]query engineer by idcode = %s'%idcode)
		tablename =queryTableNameByTerminalId(terminalId,'MAINTER')
		tablename = tablename.encode('utf-8')
		log.debug('tablename=%s'%tablename)
		m = MaintenancePerson.new(tablename)
		log.debug(m)
		man = m.objects.filter(idno=idcode)
		log.debug('[1]query size = %d'%len(man))
		if len(man) > 0 :
			log.debug('[DBQUERY]name=%s'%man[0].name );
			return man[0].name
		else:
			log.debug('[DBQUERY]no record')
			return ''
	except Exception,err:
		log.debug('[1]query fail:%s'%err)
		return ''




def queryTableNameByCode(code  , identity):
	try:
		l = BankCodeTable.objects.filter(bankCode=code , mark=identity)
		if len(l) > 0 :
			#log.debug('[DBQUERY]tablename=%s'%l[0].tableName );
			return l[0].tableName
		else:
			log.debug('[DBQUERY]no record')
			return ''
	except Exception , err:
		log.debug('[2]query fail:%s'%err)
		return ''	
	

def queryTableNameByTerminalId(terminalId  , identity):
	try:
		terminals = Terminal.objects.filter(terminalId=terminalId)
		if len(terminals) > 0 :
			#log.debug('[DBQUERY]tablename=%s'%l[0].tableName );
			l = BankCodeTable.objects.filter(bankCode=terminals[0].bankCode , mark=identity)
			if len(l) > 0 :
				return l[0].tableName
			else:
				return ''
		else:
			log.debug('[DBQUERY]no record')
			return ''
	except Exception , err:
		log.debug('[2]query fail:%s'%err)
		return ''	


