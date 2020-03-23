from models import sys as sysdb
from django.shortcuts import render

def fetchQuestion(request):
	v = {"question":{"label":"test","index":1}}
	return render(request , 'mobile/edu/templates/q001.html',v)
	
