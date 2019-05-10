# -*- coding:utf8 -*-
from django.http import JsonResponse
import logging
import traceback
from drsys import face,cnn
import cv2
import numpy
import uuid
from drconf import dr
import os
from PIL import Image
from io import BytesIO
from drers import models
from drers import utils as du
from drsys import syntask


log = logging.getLogger('DR') 



def confirmNewFace(request):#confirm the face is select for new face into db
	if request.method == 'POST':
		try:
			idcode = request.POST.get('idcode')
			terminalId = request.POST.get('terminalId')
			personType = request.POST.get('personType')
			log.debug('post param idcode = %s'%idcode)
			
			imgPath = '%s%s'%(dr.PROJECT_BASE , request.POST.get('faceimg').encode(dr.ENCODING))
			log.debug(' faceimg1 = %s'%imgPath)
						
			ret = du.learnNewFace(terminalId , idcode , imgPath ,personType)
			if ret.find("succ")>=0:
				#syntask.drSyn(face._train_)
				#log.debug('training')
				msg = {"result":True,"msg":"learn succ"}
			else:
				msg = {"result":False,"msg":"learn fail[%s]"%idcode}
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		except Exception,err:
			log.debug('err=%s'%err)
			msg = {"result":False,"msg":"%s"%err}	
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})


def onlyFaceUploadByIdCode(request):
	if request.method == 'POST':
		
		try:
			img = request.FILES.get('idimg')
			idcode = request.GET.get('idcode','')

			terminalId = request.GET.get('terminalId','')
			personType = request.GET.get('personType','')

			personExists = models.checkPersonByIDCode(terminalId , idcode , personType)
			msg={}
			if personExists :
			
				tmpFilename = '%s.jpg'%(uuid.uuid1())
				savePath = '%s/%s'%(dr.FACETMP,tmpFilename)

				#get idcode param
				req_param_idcode = request.GET.get('idcode')
				log.debug('request param idcode = %s'%req_param_idcode)						
				
				#face pick and store tmp file\
				imgData = img.read()
				faceimg = face.pickFaceFromBytes(imgData)
				cv2.imwrite(savePath , faceimg)
			
				log.debug('file upload at %s'%savePath)
			
			
				msg = {"result":True,"msg":"succ","idcode":"%s"%idcode,"faceimg":"%s"%savePath.replace(dr.PROJECT_BASE,'')}
			else:
				msg = {"result":False,"msg":"noauth"}		
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		except Exception,err:
			log.debug('err=%s'%traceback.format_exc())
			msg = {"result":False,"msg":"%s"%err}					
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		
	else:
		log.debug('error request method')
		return JsonResponse({'result':False},json_dumps_params={'ensure_ascii':False})


			
def faceUploadAndCheck(request):
	if request.method == 'POST':
		try:
			img = request.FILES.get('idimg')
			
			terminalId = request.GET.get('terminalId','')
			personType = request.GET.get('personType','ENG')
			tmpFilename = '%s.jpg'%(uuid.uuid1())
			savePath = '%s/%s'%(dr.FACETMP,tmpFilename)
						
			#get terminalId param
			req_param_terminalId = request.GET.get('terminalId')
			log.debug('request param terminalId = %s'%req_param_terminalId)
				
			#face pick and store tmp file\
			imgData = img.read()
			faceimg = face.pickFaceFromBytes(imgData)
			cv2.imwrite(savePath , faceimg)
			
			log.debug('file upload at %s'%savePath)

			ret = face.checkFace(savePath ,terminalId , personType)
			log.debug('face check RET %s'%ret)
			if len(ret)==0:
				ret = 'Nobody'
			log.debug('ret=%s'%ret)
			if  ret.find("Nobody")>=0 or ret.find("fail")>=0 :
				
				msg = {"result":False,"msg":"%s"%ret}
			else:
				retName = models.queryEngineerNameByIdno(req_param_terminalId,ret)
				retName = retName.encode(dr.ENCODING)
				msg = {"result":True,"msg":"%s"%retName,"idcode":"%s"%ret,"faceimg":"%s"%savePath.replace(dr.PROJECT_BASE,'')}
				
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		except Exception,err:
			log.debug('err=%s'%traceback.format_exc())
			msg = {"result":False,"msg":"%s"%err}					
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		
	else:
		log.debug('error request method')
		return JsonResponse({'result':False},json_dumps_params={'ensure_ascii':False})



def idFaceImg(request):
	if request.method == 'POST':
		try:
			img = request.FILES.get('img')
			idcode = request.GET.get('idcode','')
			terminalId = request.GET.get('terminalId','')
			personType = request.GET.get('personType','')

			personExists = models.checkPersonByIDCode(terminalId , idcode , personType)
			msg = {}
			if personExists :
				

				idx = models.queryPersonFacePath(terminalId,idcode);
				log.debug("idcode=%s,idx=%s"%(idcode,idx))
				savePath = os.path.join(dr.FACESET , idx)
				if not os.path.exists(savePath):
					os.makedirs(savePath)
				imgData = img.read()
				faceimg = face.pickFaceFromBytes(imgData)

				_id_img_filepath = os.path.join(savePath,"0001.jpg")
			
				if not os.path.exists(_id_img_filepath):
					cv2.imwrite(_id_img_filepath , faceimg)
					log.debug('file upload at %s'%savePath)
					syntask.drSyn(face._train_)
					log.debug('training')
				else:
					log.debug('file exists,nothing is changed')
			
				msg = {"result":True,"msg":"%s"%_id_img_filepath}
			else:
				msg = {"result":False,"msg":"noauth"}	
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		except Exception,err:
			log.debug('err=%s'%err)
			msg = {"result":False,"msg":"%s"%err}					
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})	
	else:
		log.debug('error request method')
		return JsonResponse({'result':False},json_dumps_params={'ensure_ascii':False})
