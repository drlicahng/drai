#! /usr/bin/env python
# -*- coding:utf8 -*-
from drconf import single,dr
import sys
import logging
from drsys import cnn,drdlib,facedb,face
from drers import models , utils as du
import pandas as pd
import numpy as np

from services.edu import ques

log = logging.getLogger(dr.TAG) 

if __name__ == "__main__":
	log.debug('shell is run[param has %s]'%len(sys.argv))
	cmdFunc = sys.argv[1]
	log.debug('shell command called:%s'%cmdFunc)
	#param
	param = []
	
	if cmdFunc.find('train')>=0:#ai trainer(CNN) param0 = bankCode   param1 = ENG|EMP   (engineer or employee)
		param.append(sys.argv[2])#bankCode
		param.append(sys.argv[3])#person type
		log.debug('a train[%s] will console'%param[0])
		
		'''dataset = cnn.DataSet(param[0],param[1])
    		model = cnn.Model()
    		model.read_trainData(dataset)
    		model.build_model()
    		model.train_model()
    		model.evaluate_model()
    		model.save()'''
		face._train_special(param[0] , param[1])

	elif cmdFunc.find('test')>=0:#normal test main exec
		param.append(sys.argv[2])
		if param[0].find('face')>=0:
			name = cnn.KerasFace('10:d0:7a:01:a8:50','ENG').matchFace('/home/dr/my.jpg')
    			print name
		elif param[0].find('models')>=0:
			has = models.checkEMPByIDCode('422202198006160057')
			print has
		elif param[0].find('learnNew')>=0:
			ret = du.learnNewFace('10:d0:7a:1d:97:3c','422202198006160057','/faceimg/04c59ed4-761b-11e9-8c98-6c92bf4f8706.jpg','EMP')
			print ret
		elif param[0].find('mongodb')>=0:
		
			for v in ques.nextQuestion():
				print v.author.name

	elif cmdFunc.find('dlib')>=0:#dlib function test cmd
		param.append(sys.argv[2])
		print param[0]
		if param[0].find('_init_')>=0:
			print 'ere'
		elif param[0].find('match')>=0 :#pick a face from a image and save the face img into a file
			param.append(sys.argv[3])#source image abs image file path
			param.append(sys.argv[4])#the path of face image should be to compare
			result = drdlib.matchFace(param[1] ,param[2])
			print result
	elif cmdFunc.find('dr')>=0:
		param.append(sys.argv[2])
		if param[0].find('test')>=0:
			param.append(sys.argv[3])#dr test [param1]
			data = facedb.read_faces(param[1])
			
			facedb.save('/home/dr/test.csv',data)
			#print data[0]
			
			#csvOper = pd.DataFrame(columns=None , data=data)
			#csvOper.to_csv('/home/dr/test.csv',encoding='utf8')
			#pd.set_option('display.max_columns',10000,'display.max_rows',10000)
			#csvOper = pd.read_csv('/home/dr/test.csv',dtype={'0':'object'})
			#print csvOper
			
			
			
			#labels , data = facedb.load('/home/dr/test.csv')
			#print labels
			#print data

		elif param[0].find('face')>=0:
			param.append(sys.argv[3])#input face file path
			param.append(sys.argv[4])#terminalId
			param.append(sys.argv[5])#personType
			label , pre= facedb.matchFace(param[1] , param[2] , param[3])
			if pre < 1 :
				print 'is %s[%s]'%(label,pre)
			else:
				print 'nobody matched[pre=%s]'%pre
			
		elif param[0].find('train')>=0:#eg train DRJF ENG
			param.append(sys.argv[3])#bankcode
			param.append(sys.argv[4])#personType
		
			facedb._train(param[1] , param[2])
		elif param[0].find('match')>=0:
			param.append(sys.argv[3])#matchImagePath
			param.append(sys.argv[4])#terminalId
			param.append(sys.argv[5])#idcode
			param.append(sys.argv[6])#personType		
			pre = face._checkFace(param[1] , param[2] , param[3],param[4])
			print pre
			
