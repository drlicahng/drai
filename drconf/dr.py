ENCODING='utf8'

datefmt = '%Y-%m-%d %H:%M:%S'

#log tag
TAG='DR'

#web
PROJECT_BASE= '/home/dr/drai'

#face
FACE_BASE='%s'%PROJECT_BASE
FACESET = '%s/faceset'%FACE_BASE
ENGINEER_FACESET = '%s/ENG'%FACESET
EMPLOYEE_FACESET = '%s/EMP'%FACESET
FACETMP = '%s/faceimg'%FACE_BASE
MAX_LEARN_SELF_NUM = 30

FACE_CLASSIFIER = 'drsys/haarcascade_frontalface_alt2.xml'

FACE_MODEL_FILES_DIR = '%s/files'%PROJECT_BASE

FACE_SIZE = 128

#voice
WAV_MIN_LENGTH = 512
VOICETMP = '%s/voice'%PROJECT_BASE
