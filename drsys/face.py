# -*- coding:utf8 -*-
import math
import cv2
from sklearn import neighbors
import os
import os.path
from io import BytesIO
import sys
import pickle
import numpy as np
from PIL import Image, ImageDraw,ImageFont
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import time
import logging
from drconf import dr
import shutil
from drsys import syntask
import trainer
from drsys import cnn
from drsys import facedb
from drsys import drdlib
from drers import models

reload(sys)
sys.setdefaultencoding('utf-8')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','bmp'}
log = logging.getLogger(dr.TAG) 

train_file = '%s/trained_knn_model.clf'%dr.FACE_BASE

#knn train function
def _train_():
	#log.debug("Training KNN classifier...")
	#classifier = trainer._init_train("faceset", model_save_path="%s/trained_knn_model.clf"%dr.PROJECT_BASE, n_neighbors=2)
	#log.debug("Training complete!")
	'''dataset = DataSet('DRJF','ENG')
    	model = Model()
    	model.read_trainData(dataset)
    	model.build_model()
    	model.train_model()
    	model.evaluate_model()
    	model.save()'''
	#drjf train
	facedb._train('DRJF','ENG')

def _train_special(bankcode , personType):
	facedb._train(bankcode , personType)


def getfaces(img):
	return face_recognition.face_locations(img)#pick face by face_recognition


def pickFaceFromBytes(data):
	pilImage = Image.open(BytesIO(data))
	cvImage = np.array(pilImage)
	#cvImage = cv2.cvtColor(cvImage , cv2.COLOR_RGB2BGR)
	face_locations = getfaces(cvImage)

	for face_location in face_locations:
		top,right,bottom,left =  face_location
    		face_img = cvImage[top:bottom,left:right]
		return face_img

	return np.array([])


def pickFaceFromFile(f):
	cvImage = cv2.imread(f)
	cvImage = cv2.cvtColor(cvImage , cv2.COLOR_RGB2BGR)
	face_locations = getfaces(cvImage)

	for face_location in face_locations:
		top,right,bottom,left =  face_location
    		face_img = cvImage[top:bottom,left:right]
		return face_img

	return np.array([])


def lastFace(facePath):
	try:

		return True
	except Exception ,err:
		log.debug('fail:%s'%err)
		return False


def checkFace(tmpFile ,terminalId ,personType):
	#try:
		#name = cnn.KerasFace('10:d0:7a:01:a8:50','ENG').matchFace(tmpFile)
		name ,precision = facedb.matchFace(tmpFile , terminalId ,personType)
		log.debug('checkface result is %s[%s]'%(name,precision))
		return name
	#except Exception,err:
		#log.debug('fail:%s'%err)
		#return 'fail:%s'%err

def _checkFace(tmpFile , terminalId , idcode , personType):
	log.debug('image file match the id image')
	idx = models.queryIndeByTerminalId(terminalId)
	FILE_PATH = ''
	if personType == 'ENG':
		FILE_PATH = '%s/ENG/%s/%s/0001.jpg'%(dr.FACESET , idx , idcode)
	else:
		FILE_PATH = '%s/EMP/%s/%s/0001.jpg'%(dr.FACESET , idx , idcode)
	log.debug('id image location:%s'%FILE_PATH)
	return facedb._only_matchFace_(tmpFile , FILE_PATH)


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):
    
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("NOT FOUND KNN MODEL FILE")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def lookFromDir(path):
	result=[]
	start = time.clock()
	for image_file in os.listdir(path):
        	full_file_path = os.path.join(path, image_file)
 
        	predictions = predict(full_file_path, model_path=train_file)

        	for name, (top, right, bottom, left) in predictions:
            		log.debug("- Found {} at ({}, {})".format(name, left, top))
			result.append(name)
	end = time.clock()
	log.debug( 'cost %s second'%(end-start))
	print result


def lookFromImageFile(filepath):
	
        full_file_path = filepath
	start = time.clock()
        
        predictions = predict(full_file_path, model_path=train_file)
	end = time.clock()
	log.debug( 'cost %s second'%(end-start) )
        for name, (top, right, bottom, left) in predictions:
            log.debug("- Found {} at ({}, {})".format(name, left, top))
	    return name

if __name__ == "__main__":
    name = lookFromImageFile('test/my.jpg')
    print 'found %s'%name
    
