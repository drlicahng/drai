from django.conf.urls import *
import index
from drers import voice
from web import http
from drers import doUpload
from drers import websys
urlpatterns = [
	url('^hello/$',index.hello),
	url('^index/$',index.index),
	url('^upload.dr/$',http.idImageUpload),
	url('^getVoice/$',voice.getVoice),
	url('^faceUpload/$',doUpload.faceImg),
	url('^idface/$',doUpload.idFaceImg),
	url('^confirmNewFace/$',doUpload.confirmNewFace),
	url('^drsys/train/$',websys.train),
]
