from drconf import single
import cv2
from PIL import Image
from drsys import face
from models.faceid import Face

im = cv2.imread('/home/dr/idcode.bmp',1)

img = Image.fromarray(im.astype('uint8')).convert('RGB')

f = Face(idcode='422202198006160057');
f.img = img
f.save()
#face.saveImage(f.img,'/home/dr/t.bmp')
