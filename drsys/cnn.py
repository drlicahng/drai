#-*-coding:utf8-*-
#single run, cut when run with server
from drconf import single,dr
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
import random
from keras.models import Sequential,load_model
from keras.layers import Dense,Activation,Convolution2D,MaxPooling2D,Flatten,Dropout
from drers import models

import logging

log = logging.getLogger('DR') 


def read_file(path):
    img_list = []
    label_list = []
    dir_counter = 0
    IMG_SIZE = 128

   
    for child_dir in os.listdir(path):
         child_path = os.path.join(path, child_dir)
	 if os.path.isfile(child_path):
	     continue
         for dir_image in  os.listdir(child_path):
             if dir_image.endswith('jpg'):
                img = cv2.imread(os.path.join(child_path, dir_image))
                resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                recolored_img = cv2.cvtColor(resized_img,cv2.COLOR_BGR2GRAY)
                img_list.append(recolored_img)
                label_list.append(dir_counter)

         dir_counter += 1

   
    img_list = np.array(img_list)

    return img_list,label_list,dir_counter


def read_name_list(path):
    name_list = []
    print 'path=%s'%path
    if os.path.isfile(path):
	return name_list
    for child_dir in os.listdir(path):
	if os.path.isfile(child_dir):
		continue
        name_list.append(child_dir)
    return name_list




#建立一个用于存储和格式化读取训练数据的类
class DataSet(object):
   DATA_PATH = ''
   def __init__(self,bankCode,personType='ENG'):
        self.num_classes = None
	self.X_train = None
	self.X_test = None
	self.Y_train = None
	self.Y_test = None
	self.img_size = dr.FACE_SIZE

	idx = models.queryIndeByBankCode(bankCode)
	print idx
	if personType == 'ENG':
		self.DATA_PATH = '%s/%s'%(dr.ENGINEER_FACESET,idx)	
	else:
		self.DATA_PATH = '%s/%s'%(dr.EMPLOYEE_FACESET,idx)
	print self.DATA_PATH
	self.extract_data(self.DATA_PATH) #在这个类初始化的过程中读取path下的训练数据

   def extract_data(self,path):
        #根据指定路径读取出图片、标签和类别数
        imgs,labels,counter = read_file(path)

        #将数据集打乱随机分组
        X_train,X_test,y_train,y_test = train_test_split(imgs,labels,test_size=0.2,random_state=random.randint(0, 100))

        #重新格式化和标准化
        # 本案例是基于thano的，如果基于tensorflow的backend需要进行修改
        X_train = X_train.reshape(X_train.shape[0], self.img_size, self.img_size,1)/255.0
        X_test = X_test.reshape(X_test.shape[0],  self.img_size, self.img_size,1) / 255.0

        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')

        #将labels转成 binary class matrices
        Y_train = np_utils.to_categorical(y_train, num_classes=counter)
        Y_test = np_utils.to_categorical(y_test, num_classes=counter)

        #将格式化后的数据赋值给类的属性上
        self.X_train = X_train
        self.X_test = X_test
        self.Y_train = Y_train
        self.Y_test = Y_test
        self.num_classes = counter

   def check(self):
       print('num of dim:', self.X_test.ndim)
       print('shape:', self.X_test.shape)
       print('size:', self.X_test.size)

       print('num of dim:', self.X_train.ndim)
       print('shape:', self.X_train.shape)
       print('size:', self.X_train.size)

#建立一个基于CNN的人脸识别模型
class Model(object):
    FILE_PATH = "model.dr"   #模型进行存储和读取的地方
    PATH = ''
    IMAGE_SIZE = 128    #模型接受的人脸图片一定得是128*128的

    def __init__(self):
        self.model = None

    #读取实例化后的DataSet类作为进行训练的数据源
    def read_trainData(self,dataset):
        self.dataset = dataset
	if self.dataset.DATA_PATH.find('ENG')>=0:
		self.FILE_PATH = '%s/ENG.dr'%(self.dataset.DATA_PATH.replace('ENG','models'))
	else:
		self.FILE_PATH = '%s/EMP.dr'%(self.dataset.DATA_PATH.replace('EMP','models'))
	print 'init path at %s'%self.FILE_PATH

    #建立一个CNN模型，一层卷积、一层池化、一层卷积、一层池化、抹平之后进行全链接、最后进行分类
    def build_model(self):
        self.model = Sequential()
        self.model.add(
            Convolution2D(
                filters=32,
                kernel_size=(5, 5),
                padding='same',
                dim_ordering='th',
                input_shape=self.dataset.X_train.shape[1:]
            )
        )

        self.model.add(Activation('relu'))
        self.model.add(
            MaxPooling2D(
                pool_size=(2, 2),
                strides=(2, 2),
                padding='same'
            )
        )
        

        self.model.add(Convolution2D(filters=64, kernel_size=(5, 5), padding='same'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
        

        self.model.add(Flatten())
        self.model.add(Dense(512))
        self.model.add(Activation('relu'))
        

        self.model.add(Dense(self.dataset.num_classes))
        self.model.add(Activation('softmax'))
        self.model.summary()

    #进行模型训练的函数，具体的optimizer、loss可以进行不同选择
    def train_model(self):
        self.model.compile(
            optimizer='adam',  #有很多可选的optimizer，例如RMSprop,Adagrad，你也可以试试哪个好，我个人感觉差异不大
            loss='categorical_crossentropy',  #你可以选用squared_hinge作为loss看看哪个好
            metrics=['accuracy'])

        #epochs、batch_size为可调的参数，epochs为训练多少轮、batch_size为每次训练多少个样本
        self.model.fit(self.dataset.X_train,self.dataset.Y_train,epochs=15,batch_size=32)

    def evaluate_model(self):
        print('\nTesting---------------')
        loss, accuracy = self.model.evaluate(self.dataset.X_test, self.dataset.Y_test)

        print('test loss;', loss)
        print('test accuracy:', accuracy)

    def save(self):
        print('Model Saved at %s.'%self.FILE_PATH)
	if not os.path.exists(self.FILE_PATH[0:-6]):
		os.makedirs(self.FILE_PATH[0:-6])
	
        self.model.save(self.FILE_PATH)

    def load(self,terminalId='',personType='ENG'):
        idx = models.queryIndeByTerminalId(terminalId)
	
	if personType == 'ENG':
		self.FILE_PATH = '%s/models/%s/ENG.dr'%(dr.FACESET,idx)
		self.PATH = '%s/%s'%(dr.ENGINEER_FACESET,idx)	
	else:
		self.FILE_PATH = '%s/models/%s/EMP.dr'%(dr.FACESET,idx)
		self.PATH = '%s/%s'%(dr.EMPLOYEE_FACESET,idx)
        self.model = load_model(self.FILE_PATH)
	print('Model Loaded.%s'%self.FILE_PATH)

    #需要确保输入的img得是灰化之后（channel =1 )且 大小为IMAGE_SIZE的人脸图片
    def predict(self,img):
	
        img = img.reshape((1, self.IMAGE_SIZE, self.IMAGE_SIZE,1))
        img = img.astype('float32')
        img = img/255.0

        result = self.model.predict_proba(img)  #测算一下该img属于某个label的概率
        max_index = np.argmax(result) #找出概率最高的

        return max_index,result[0][max_index] #第一个参数为概率最高的label的index,第二个参数为对应概率



#=================test
class KerasFace(object):
   
    PATH = ''
    def __init__(self,terminalId='',personType='ENG'):
        self.model = Model()
        self.model.load(terminalId,personType=personType)
        #self.img_size = 128


    def matchFace(self,imgFile):
	
        #opencv文件中人脸级联文件的位置，用于帮助识别图像或者视频流中的人脸
        face_cascade = cv2.CascadeClassifier(dr.FACE_CLASSIFIER)
        #读取dataset数据集下的子文件夹名称
        name_list = read_name_list(self.model.PATH)

        img=cv2.imread(imgFile)
	#img = face.pickFaceFromFile('/home/dr/my2.bmp')
        #打开摄像头并开始读取画面
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #图像灰化
        #faces = face_cascade.detectMultiScale(gray, 1.3, 5)#识别人脸
        #print len(faces)
        #for (x, y, w, h) in faces:
            #ROI = gray[x:x + w, y:y + h]
        gray = cv2.resize(gray, (dr.FACE_SIZE, dr.FACE_SIZE), interpolation=cv2.INTER_LINEAR)
        label,prob = self.model.predict(gray)  #利用模型对cv2识别出的人脸进行比对
	print 'name=%s,prob=%s'%(name_list[label],prob)
        if prob >0.9:    #如果模型认为概率高于70%则显示为模型中已有的label
        	show_name = name_list[label]
        else:
                show_name = 'Nobody'
        return show_name
        #cv2.putText(img, show_name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)  #显示名字
        #img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  #在人脸区域画一个正方形出来
        #cv2.imshow("face", img)
        #cv2.waitKey(0)




if __name__ == '__main__':
    
    '''dataset = DataSet('DRJF','ENG')
    model = Model()
    model.read_trainData(dataset)
    model.build_model()
    model.train_model()
    model.evaluate_model()
    model.save()'''
    name = KerasFace('10:d0:7a:01:a8:50','ENG').matchFace('/home/dr/tmp.jpg')
 
    print name

