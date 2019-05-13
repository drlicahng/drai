# -*- coding:utf8 -*-
from django.db import models
import logging
from drconf import dr
log = logging.getLogger(dr.TAG)

 

class SysOrgan(models.Model):
	class Meta:
		db_table = 'departments'
	id = models.AutoField(primary_key=True , db_column='id')
	departmentId = models.OneToOneField('SysOrgan' , to_field='id')
	name = models.CharField(max_length=60)
	sort = models.IntegerField()
	address = models.CharField(max_length=100)
	header = models.CharField(max_length=50)
	mobile = models.CharField(max_length=50)
	phone = models.CharField(max_length=50)
	bankCode = models.CharField(max_length=10)
	treeId = models.CharField(max_length=255)
	appId = models.CharField(max_length=60)
	secret = models.CharField(max_length=100)

class SysUser(models.Model):
	class Meta:
		db_table = 'users'
	

	id = models.AutoField(primary_key=True , db_column='id')
	departmentId = models.OneToOneField('SysOrgan' , to_field='id')
	name = models.CharField(max_length=50)
	sex = models.CharField(max_length=10)
	login = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	moNumber = models.CharField(max_length=50)
	shortNumber = models.CharField(max_length=50)
	inTime = models.DateTimeField()
	outTime = models.DateTimeField()
	roleIds = models.CharField(max_length=200)
	phone = models.CharField(max_length=20)
	idcode = models.CharField(max_length=30)

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


	id = models.AutoField(primary_key=True , db_column='id')
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
	

	id = models.AutoField(primary_key=True , db_column='id')
	bankCode = models.CharField(max_length=10)
	tableName = models.CharField(max_length=50)
	mark = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	content = models.CharField(max_length=100)


class DRAuth(models.Model):
	class Meta:
		db_table = 'DR_BANKCODE_AUTH'
	

	id = models.AutoField(primary_key=True , db_column='id')
	bankCode = models.CharField(max_length=10)
	drIndentity = models.IntegerField()
	




class Terminal(models.Model):
	class Meta:
		db_table = 'departterminal'
	

	id = models.AutoField(primary_key=True , db_column='id')
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



#db function
def queryEngineerNameByIdno(terminalId , idcode):
	try:
		log.debug('[DBQUERY]query engineer by idcode = %s'%idcode)
		log.debug('terminalId=%s'%terminalId)
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
		log.debug('[3]query fail:%s'%err)
		return ''	


def queryBankCodeByTerminalId(terminalId):
	try:
		terminals = Terminal.objects.filter(terminalId=terminalId)
		if len(terminals) > 0 :
			return terminals[0].bankCode
		else:
			log.debug('[DBQUERY]no record')
			return ''
	except Exception , err:
		log.debug('[3]query fail:%s'%err)
		return ''


def queryIndeByTerminalId(terminalId):
	try:
		bankCode = queryBankCodeByTerminalId(terminalId)
		print bankCode
		return queryIndeByBankCode(bankCode)
	except Exception,err:
		log.debug('[4]query fail:%s'%err)
		return -2	

def queryIndeByBankCode(bankCode):
	try:
		if len(bankCode) > 0:
			idx = DRAuth.objects.filter(bankCode=bankCode)
			if len(idx) > 0:
				return idx[0].drIndentity
			else:
				return -3
		else:
			return -1
	except Exception,err:
		log.debug('[4]query fail:%s'%err)
		return -2	


def queryPersonFacePath(terminalId , idcode , personType='ENG'):
	try:
		idx = queryIndeByTerminalId(terminalId)
		if idx<=0 :
			return ''
		return '%s/%s/%s'%(personType,idx,idcode)
	except Exception , err:
		log.debug('query fail:%s'%err)
		return ''


def checkPersonByIDCode(terminalId , idcode , personType):
	if personType.find('ENG')>=0:
		return checkENGByIDCode(terminalId , idcode)
	else:
		return checkEMPByIDCode(idcode)


def checkEMPByIDCode(idcode):
	try:
		users = SysUser.objects.filter(idcode=idcode)
		if len(users) > 0:
			return True
		else:
			return False
	except Exception , err:
		log.debug('query fail:%s'%err)
		return False


def checkENGByIDCode(terminalId , idcode):
	try:
		name =queryEngineerNameByIdno(terminalId , idcode)
		if len(name) == 0:
			return False
		else:
			return True
	except Exception , err:
		log.debug('query fail:%s'%err)
		return False



'''def queryPersonFacePath(terminalId , idcode):
	try:
		idx = queryIndeByTerminalId(terminalId)
		if idx<=0 :
			return ''
		bankCode = queryBankCodeByTerminalId(terminalId)
		if len(bankCode)==0 :
			return ''
		name = queryEngineerNameByIdno(terminalId , idcode)
		if len(name)==0 :
			users = SysUser.objects.filter(idno=idcode)
			if len(users) > 0:
				return 'EMP/%s/%s'%(idx,idcode)
			else:
				return ''
		else:
			return 'ENG/%s/%s'%(idx,idcode)
	except Exception , err:
		log.debug('query fail:%s'%err)
		return '''''
