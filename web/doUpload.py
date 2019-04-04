# -*- encoding:utf-8 -*-
from django.http import JsonResponse
import logging
from drsys import face
import cv2
import numpy
import uuid
from drconf import dr
import os
from PIL import Image
from io import BytesIO
from drers import models

log = logging.getLogger('DR') 

def faceImg(request):
	if request.method == 'POST':
		
		try:
			img = request.FILES.get('idimg')
			tmpFilename = '%s.jpg'%(uuid.uuid1())
			savePath = '%s/%s'%(dr.FACETMP,tmpFilename)
			
			#face pick and store tmp file\
			imgData = img.read()
			faceimg = face.pickFaceFromBytes(imgData)
			cv2.imwrite(savePath , faceimg)
			'''with open(savePath , 'wb+') as out:
				for chunk in img.chunks():
					out.write(chunk)'''
			log.debug('file upload at %s'%savePath)
			ret = face.checkFace(savePath)
			log.debug('face check RET %s'%ret)
			log.debug('cond1=%d'%(ret.find("unknown")))
			log.debug('cond2=%d'%(ret.find("fail")))
			if ret.find("unknown")>=0 or ret.find("fail")>=0 :
				
				msg = {"ret":"fail","msg":"%s"%ret}
			else:
				retName = models.queryEngineerNameByIdno('ICBC',ret)
				msg = {"ret":"succ","msg":"%s"%retName,"idcode":"%s"%ret,"faceimg":"%s"%savePath.replace(dr.PROJECT_BASE,'')}
				
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		except Exception,err:
			log.debug('err=%s'%err)
			msg = {"ret":"fail","msg":"%s"%err}					
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		
	else:
		log.debug('error request method')
		return JsonResponse({'ret':'fail'},json_dumps_params={'ensure_ascii':False})



def idFaceImg(request):
	if request.method == 'POST':
		try:
			img = request.FILES.get('img')
			idcode = request.GET.get('idcode')
			log.debug(idcode)
			savePath = '%s/%s/'%(dr.FACESET , idcode)
			if not os.path.exists(savePath):
				os.makedirs(savePath)
			imgData = img.read()
			faceimg = face.pickFaceFromBytes(imgData)

			_id_img_filepath = "%s0001.jpg"%(savePath)
			'''with open(_id_img_filepath , 'wb+') as out:
				for chunk in img.chunks():
					out.write(chunk)'''
			if not os.path.exists(_id_img_filepath):
				cv2.imwrite(_id_img_filepath , faceimg)
				log.debug('file upload at %s'%savePath)
			else:
				log.debug('file exists,nothing is changed')
			
			msg = {"result":True,"msg":"%s"%_id_img_filepath}	
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		except Exception,err:
			log.debug('err=%s'%err)
			msg = {"result":False,"msg":"%s"%err}					
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})	
	else:
		log.debug('error request method')
		return JsonResponse({'result':False},json_dumps_params={'ensure_ascii':False})
