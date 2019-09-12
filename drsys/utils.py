#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
import datetime
import time
#from drconf import dr


#return the dir' all sub file, sort by file modified time
def listFileByTime(dir_path):
	dir_list = os.listdir(dir_path)
	if not dir_list:
		return []
	else:
		dir_list = sorted(dir_list , key=lambda x: os.path.getmtime(os.path.join(dir_path,x)) , reverse=True)
		return dir_list


#return the name of file without ext
#eg: input : test.jpg  return test
def getFileNameWithoutExt(filename):
	index = filename.rfind('.')
	return filename[:index]




#number to the length'S string
def int2str(num , length=2 , fix='0' , align='l'):
	strnum = '%d'%num
	if len(strnum) < length:
		for n in range(0 , (length - len(strnum))):
			if align == 'r':
				strnum = '%s%s'%(strnum,fix)			
			else:
				strnum = '%s%s'%(fix,strnum)
		return strnum
	else:
		return strnum

'''
datetime method

'''
def fmtMTime(t):
	mtime = time.localtime(t)
	return '%d-%d-%d %d:%d:%d'%(mtime.tm_year , mtime.tm_mon , mtime.tm_mday , mtime.tm_hour , mtime.tm_min , mtime.tm_sec)


if __name__ == '__main__':
	dir_path = '/home/dr/drai/faceset/ENG/200/422202198006160057'
	l = listFileByTime(dir_path)
	

	print l


