# -*- coding:utf8 -*-
from django.http import JsonResponse
import logging
from drsys import facedb

log = logging.getLogger('DR') 

def train(request):
	bankCode = ''
	personType = ''
	
	if request.method == 'POST':
		try:
			bankCode = request.POST.get('bankCode','')
			personType = request.POST.get('personType','')
		except Exception , err:
			log.debug('err=%s'%err)
			msg = {"result":False,"msg":"%s"%err}	
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
	else:
		try:
			bankCode = request.GET.get('bankCode','')
			personType = request.GET.get('personType','')
		except Exception , err:
			log.debug('err=%s'%err)
			msg = {"result":False,"msg":"%s"%err}	
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})

	if len(bankCode) > 0 and len(personType)>0:
		facedb._train(bankCode , personType)
		msg = {"result":True,"msg":"train completed"}	
		return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
	else:
		log.debug('param is not allow none')
		msg = {"result":False,"msg":"param is null"}	
		return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
