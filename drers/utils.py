# -*- encoding:utf-8 -*-
import os
from drconf import dr
from drsys import utils as du
import shutil
import logging

log = logging.getLogger(dr.TAG) 

def learnNewFace(idcode , imgpath):
	_the_face_set_dir = os.path.join(dr.FACESET , idcode)

	_list_face_img_path = du.listFileByTime(_the_face_set_dir)
	log.debug('the person[%s] had %d faces'%(idcode,len(_list_face_img_path)))
	_new_img_file_index = 2
	print(_list_face_img_path)

	if len(_list_face_img_path) > 1 :
		_last_img_file_name = du.getFileNameWithoutExt(_list_face_img_path[-1])
		log.debug('faceset last face is %s'%_last_img_file_name)
		_new_img_index = int(_last_img_file_name) + 1
		if _new_img_index > dr.MAX_LEARN_SELF_NUM : 
			_new_img_index = 2
		
		_new_img_filename = "%s.jpg"%du.int2str(_new_img_index, length=4)
		log.debug('the new face img name is %s' % _new_img_filename)
		_new_img_file_path = os.path.join(dr.FACESET,idcode,_new_img_filename)
		
		shutil.copy(imgpath , _new_img_file_path)
		log.debug('the new face is create in faceset[%s]'%_new_img_file_path)
		return True
	else:
		return False
