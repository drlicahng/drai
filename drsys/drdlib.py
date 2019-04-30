# -*- coding:utf8 -*-
import dlib
import sys
import cv2
from drconf import dr
import logging
import numpy as np


log = logging.getLogger('DR') 


predictor_path = '%s/shape_predictor_68_face_landmarks.dat'%dr.FACE_MODEL_FILES_DIR
face_rec_model_path = '%s/dlib_face_recognition_resnet_model_v1.dat'%dr.FACE_MODEL_FILES_DIR


face_detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

def findFace(imgFile):#imgFile : a file path who contains bgr numpy ndarray
	#print 'dlib face data:'
	img = cv2.imread(imgFile)	
	b , g , r  = cv2.split(img) #color channel
	img = cv2.merge([r,g,b]) #build rgb image ndarray

	faces = face_detector(img ,1)
	#print 'find face %s'%len(faces)
	if len(faces):
		for index , face in enumerate(faces):
			shape = sp(img,face)
			face_desc = facerec.compute_face_descriptor(img,shape)
			#print np.array(face_desc)
			return face_desc
	else:
		return []


def _count_dist(img_dist_1 , img_dist_2):
	#return np.sqrt(sum((np.array(img_dist_1)-np. array(img_dist_2))**2))
	diff = 0
	for i in xrange(len(img_dist_1)):
		diff += (img_dist_1[i] - img_dist_2[i])**2
	diff = np.sqrt(diff)
	return diff

def matchFace(img1 , img2):
	_img1 = findFace(img1)
	_img2 = findFace(img2)
	
	count = _count_dist(_img1 , _img2)
	return count
	
