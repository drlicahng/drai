# -*- encoding:utf8 -*-
import os
from drconf import dr
from drsys import utils as du
from drers import models
import shutil
import logging

log = logging.getLogger(dr.TAG) 

def learnNewFace(terminalId , idcode , imgpath,personType='ENG'):
	log.debug('learn in')
	_the_face_set_dir = os.path.join(dr.FACESET,models.queryPersonFacePath(terminalId,idcode,personType));#os.path.join(dr.FACESET , idcode)
        log.debug('face set base in %s'%_the_face_set_dir)
	_list_face_img_path = du.listFileByTime(_the_face_set_dir)
	log.debug('the person[%s] had %d faces'%(idcode,len(_list_face_img_path)))
	_new_img_file_index = 1
	log.debug('file total has %s'%_list_face_img_path)

	if len(_list_face_img_path) > 0 :
		_last_img_file_name = du.getFileNameWithoutExt(_list_face_img_path[0])
		log.debug('faceset last face is %s'%_last_img_file_name)
		_new_img_index = int(_last_img_file_name) + 1
		if _new_img_index > dr.MAX_LEARN_SELF_NUM : 
			_new_img_index = 2
		
		_new_img_filename = "%s.jpg"%du.int2str(_new_img_index, length=4)
		log.debug('the new face img name is %s' % _new_img_filename)
		log.debug('learn idcode = %s'%idcode)
		_person_face_set_path = models.queryPersonFacePath(terminalId , idcode)
		log.debug( 'face set path = %s'%_person_face_set_path)
		_person_face_set_path = os.path.join(dr.FACESET,_person_face_set_path)
		if not os.path.exists(_person_face_set_path):
				os.makedirs(_person_face_set_path)
		_new_img_file_path = os.path.join(_person_face_set_path,_new_img_filename)
		
		shutil.copy(imgpath , _new_img_file_path)
		log.debug('the new face is create in faceset[%s]'%_new_img_file_path)
		return 'succ'
	else:
		return 'fail'
