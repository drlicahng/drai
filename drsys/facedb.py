#-*-coding:utf8-*-
#single run, cut when run with server
from drconf import dr
import os
import numpy as np
from drsys import drdlib
from drers import models
import pandas as pd
import logging
log = logging.getLogger('DR') 

def _only_matchFace_(faceImage1 , faceImage2):
	face1 = drdlib.findFace(faceImage1)
	face2 = drdlib.findFace(faceImage2)
	if len(face1)==0:
		return 2
	if len(face2)==0:
		return 3
	matchPer = drdlib._count_dist(face1 , face2)
	return matchPer

def _matchFace(faceImgFile , facedb):#BASE FUNCTION OF FACE MACTCH
	
	faceRate = 0.6	
	minIndex = 0
	_count = 1
	face =  drdlib.findFace(faceImgFile)
	log.debug("check face from %s ,found %s"%(facedb , len(face)))
	if len(face)==0:
		return '',2
	labels , data = load(facedb)
	log.debug('load model data from %s'%facedb)
	for index , d in enumerate(data):
		count = drdlib._count_dist(face , d)
		log.debug('label=%s,pre=%s,result=%s'%(labels[index] , count ,(count < faceRate)))
		if count == 0 :
			continue
		if count < _count :		
			minIndex = index
			_count = count
	#print _count
	if _count > 0.45:
		return '',1
	else:
		return labels[minIndex],_count



def matchFace(imgPath , terminalId , persontype='ENG'):#BUSS FUNCTION OF FACE MATCH
	#try:
		log.debug('face match in')
		idx = models.queryIndeByTerminalId(terminalId)
		log.debug('%s,%s,%s'%(imgPath,terminalId,persontype))		
		FILE_PATH = ''
		if persontype == 'ENG':
			FILE_PATH = '%s/models/%s/ENG.dr'%(dr.FACESET,idx)
		
		else:
			FILE_PATH = '%s/models/%s/EMP.dr'%(dr.FACESET,idx)
		log.debug('model path [%s]'%FILE_PATH)
        	result =  _matchFace(imgPath , FILE_PATH)
		log.debug(result)
		return result
	#except Exception ,err:
		#log.debug(err)
		#return '',1

def _train(bankCode , personType='ENG'):#eg: _train('DRJF','ENG')
	idx = models.queryIndeByBankCode(bankCode)
	log.debug(idx)
	if personType == 'ENG':
		DATA_PATH = '%s/%s'%(dr.ENGINEER_FACESET,idx)	
	else:
		DATA_PATH = '%s/%s'%(dr.EMPLOYEE_FACESET,idx)
	log.debug('load face from %s'%DATA_PATH)

	data = read_faces(DATA_PATH)
	
	FILE_PATH = ''
	if DATA_PATH.find('ENG')>=0:
		FILE_PATH = '%s/ENG.dr'%(DATA_PATH.replace('ENG','models'))
	else:
		FILE_PATH = '%s/EMP.dr'%(DATA_PATH.replace('EMP','models'))
	log.debug('init model path at %s'%FILE_PATH)
	if not os.path.exists(FILE_PATH[0:-6]):
		os.makedirs(FILE_PATH[0:-6])	

	save(FILE_PATH , data)

	log.debug('model trained!')



def read_faces(path):# read face data from the path (only one level subdir)
    #img_list = []
    #label_list = []
    data=[]
    
    for child_dir in os.listdir(path):
         child_path = os.path.join(path, child_dir)
	 log.debug('face read in %s'%child_path)
	 if os.path.isfile(child_path):
	     continue
         for dir_image in  os.listdir(child_path):
             if dir_image.endswith('jpg'):
		
		face_img = drdlib.findFace(os.path.join(child_path, dir_image))
                #img_list.append(np.array(recolored_img))
                #label_list.append(os.path.split(child_path)[-1])
  		#line.append(os.path.split(child_path)[-1])
		#line.append(np.array(recolored_img))
		line=[]
		imgname = os.path.split(dir_image)[-1]
		label =os.path.split(child_path)[-1] 
		line.append(label)
		log.debug('load img[%s] from %s[%s]'%(imgname,child_path,label))
		face_data = np.array(face_img)
		if len(face_data)==0:
			continue
		for d in face_data:
			line.append(d)
		#print line
		data.append(line)
    #img_list = np.array(img_list)

    return data


def save(filePath , data):# save the trained data
	csvOper = pd.DataFrame(columns=None , data=data)
	csvOper.to_csv(filePath,encoding='utf8')
	

def load(filePath):# load the trained data from the model file 
	try:
		labels = []
		data = []

		pd.set_option('display.max_columns',10000,'display.max_rows',10000)
		csvOper = pd.read_csv(filePath,dtype={'0':'object'})

		list = csvOper.values
		for line in list:
			labels.append(line[1])
			data.append(line[2:])
		return labels , data
	except Exception , err:
		log.debug(err)
		return [],[]
