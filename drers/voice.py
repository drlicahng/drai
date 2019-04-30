# -*- encoding:utf-8 -*-
from django.http import JsonResponse
from drsys import voice
from web import utils
import logging
from urllib import quote
import uuid
from drconf import dr

logger = logging.getLogger('DR') 

def getVoice(request):
	logger.debug("request in ")
	logger.debug(request.method)
	if request.method == 'POST':
		content = request.POST.get('content')
	 	logger.debug(content)

	 	token = voice.getToken()
		logger.debug("token is %s" % (token))
	 	#voiceUrl = voice.makeUrl % (token)
		logger.debug("url=%s"%voice.makeUrl)
	 	
	 	voice.voiceParam["tex"] =content
		voice.voiceParam["tok"] = token
		#param = quote(param)
	 	#logger.debug("encod token is %s" % (param["tex"]))
	 	wavData = utils.http(voice.makeUrl ,voice.voiceParam)
	 	#resp = HttpResponse(wavData)
	 	#resp['Content-Type'] = 'audio/wav'
	 	#resp['Content-Disposition'] = 'attachment;filename="tmp.wav"'
		tmpFilename = '%s.wav'%(uuid.uuid1())
		tmpfile = '%s/%s'%(dr.VOICETMP,tmpFilename)

		if len(wavData) > dr.WAV_MIN_LENGTH :
			with  open(tmpfile  , "wb") as v:
				v.write(wavData)
			msg = {"ret":"succ","url":"%s"%(tmpfile.replace(dr.PROJECT_BASE,''))}
			logger.debug(msg)
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		else:
			msg = {"ret":"fail","msg":"%s"%wavData}
			logger.debug(msg)
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		
	else:
		content = request.GET.get('content')
	 	logger.debug(content)

	 	token = voice.getToken()
		logger.debug("token is %s" % (token))
	 	#voiceUrl = voice.makeUrl % (token)
		logger.debug("url=%s"%voice.makeUrl)
	 	
	 	voice.voiceParam["tex"] =content
		voice.voiceParam["tok"] = token
		#param = quote(param)
	 	#logger.debug("encod token is %s" % (param["tex"]))
	 	wavData = utils.http(voice.makeUrl ,voice.voiceParam)
	 	#resp = HttpResponse(wavData)
	 	#resp['Content-Type'] = 'audio/wav'
	 	#resp['Content-Disposition'] = 'attachment;filename="tmp.wav"'
	 	#return resp
		tmpFilename = '%s.wav'%(uuid.uuid1())
		tmpfile = '%s/%s'%(dr.VOICETMP,tmpFilename)

		if len(wavData) > dr.WAV_MIN_LENGTH :
			with  open(tmpfile  , "wb") as v:
				v.write(wavData)
			msg = {"ret":"succ","url":"%s"%(tmpfile.replace(dr.PROJECT_BASE,''))}
			logger.debug(msg)
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})
		else:
			msg = {"ret":"fail","msg":"%s"%wavData}
			logger.debug(msg)
			return JsonResponse(msg,json_dumps_params={'ensure_ascii':False})








