ENCODING='utf8'

datefmt = '%Y-%m-%d %H:%M:%S'

#log tag
TAG='DR'

#web
PROJECT_BASE= '/home/dr/drai'

#face
FACE_BASE='%s'%PROJECT_BASE
FACESET = '%s/faceset'%FACE_BASE
FACETMP = '%s/faceimg'%FACE_BASE
MAX_LEARN_SELF_NUM = 30

#voice
WAV_MIN_LENGTH = 2048
VOICETMP = '%s/voice'%PROJECT_BASE
