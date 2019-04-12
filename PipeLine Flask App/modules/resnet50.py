import re
import numpy as np
from os import walk
from string import digits
from keras.applications import resnet50
from keras.preprocessing import image
import tensorflow as tf


class ResNet50(object):

    def __init__(self):

        self.model = resnet50.ResNet50()
        self.graph = tf.get_default_graph()

    @staticmethod
    def get_files(mypath):
        files = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            files.extend(filenames)
            break
        return files

    def get_images_array(self,path):
        images_array = [path+s for s in self.get_files(path)]
        return images_array

    def run_resnet_model(self,img_path):
        print(img_path)
        image_width = 224
        image_length = 224
        img = image.load_img(path=img_path, target_size=(image_width,image_length))
        X = image.img_to_array(img)
        X = np.expand_dims(X, axis=0)
        X = resnet50.preprocess_input(X)
        with self.graph.as_default():
            X_Pred = self.model.predict(X)
            GT_Breed = (re.search("\w+.jpg",img_path)[0])#.translate(remove_digits).replace('_.jpg',''))
            self.set_prediction(GT_Breed,resnet50.decode_predictions(X_Pred, top=3))

    def set_prediction(self,Breed,pred_class):
        predcitions = []
        for imagenet_id, name, likelihood in pred_class[0]:
            predcitions.append((name, likelihood))
            print("GT:{} - Pred: {} with {:10f} Confidence".format(Breed,name, likelihood))
        self.predcitions = predcitions

    def get_predictions(self):
        return self.predcitions

    def run_model(self,image_path):
        self.run_resnet_model(image_path)
        #for img in self.get_images_array(image_path):#"test_data/"
            #self.run_resnet_model(img)
