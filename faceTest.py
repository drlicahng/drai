from drconf import single,dr
import cv2
from PIL import Image
from drsys import face
from cnn import Model,CNN_MODEL_FILE


model = Model()
model.load_model(file_path=CNN_MODEL_FILE)

faceimg = face.pickFaceFromFile('/home/dr/szx.jpg')

faceimg = cv2.resize(faceimg , (64,64))

faceid = model.face_predict(faceimg)

print faceid


#face.saveImage(f.img,'/home/dr/t.bmp')
