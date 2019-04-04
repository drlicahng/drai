# -*- coding:utf-8 -*-
from django.http import HttpResponse
from web import utils
from drers import models
import logging
from drconf import dr
log = logging.getLogger(dr.TAG) 


def hello(request):
	name = ''
	try:
		name = models.queryEngineerNameByIdno('ICBC','422202198006160057')
		
		log.debug('name=%s'%name)
	except Exception,e:
		log.debug('fail:%s'%e)
		return HttpResponse('fail')
	return HttpResponse('ok')
