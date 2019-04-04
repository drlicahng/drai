from django.conf.urls import *
import index
import local
from web import http
from web import doUpload
urlpatterns = [
	url('^hello/$',index.hello),
	url('^upload.dr/$',http.idImageUpload),
	url('^local.a/$',local.hello),
	url('^faceUpload/$',doUpload.faceImg),
	url('^idface/$',doUpload.idFaceImg),
]
