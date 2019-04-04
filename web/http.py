from django.http import HttpResponse 
from django.shortcuts import render
import hashlib
import os


def idImageUpload(request):
	BASEDIR = os.path.dirname(os.path.dirname(__file__))
	 
	if request.method == 'POST':
		uploadData = request.FILES.get('idImg')
		f = open(os.path.join(BASEDIR , 'tmp' ,hashlib.md5(uploadData.name), uploadData.name) , 'wb')
		for chunk in uploadData.chunks():
			f.write(chunk)
		f.close()
		return HttpResponse('OK')
	return render(request , 'static/fail.html')
