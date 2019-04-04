# -*- coding:utf-8 -*-
import urllib
import urllib2
import json

def http(url , params=''):
	encUrl = url #urllib.urlencode(url)
	encData = urllib.urlencode(params)
	req = urllib2.Request(encUrl , encData)
	resp = urllib2.urlopen(req);
	
	return resp.read()



def jsonHttp(url , params=''):
	encData = urllib.urlencode(params)
	req = urllib2.Request(url , encData)
	resp = urllib2.urlopen(req);
	data = resp.read()
	return json.loads(data)
	


