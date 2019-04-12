#!/usr/bin/python
# -*- coding: utf-8 -*-

# Boiler Plate imports
import os
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt
import glob
import gc
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class YOLO(object):

    def __init__(self):
        ROOT_DIR = os.getcwd()#r'C:\Users\Ciaran\Documents\CollegeOneDrive\Year 4\FYP\Development\Flask\PipeLine Flask App' #os.getcwd()
        config = ROOT_DIR + '\\modules\\data\\yolov3.cfg'
        weights = ROOT_DIR + '\\modules\\data\\yolov3.weights'
        with open(ROOT_DIR + '\\modules\\data\\yolov3.txt', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.net = cv2.dnn.readNet(weights,config)
        self.predictions = []

    def set_image(self, image_path):
        self.image = cv2.imread(image_path)
        self.image_size = (self.image.shape[1],self.image.shape[0],0.00392)#image width, heigth, scale tuple

	#############################################
	# Object detection - YOLO - OpenCV
	# Author : Arun Ponnusamy   (July 16, 2018)
	# Website : http://www.arunponnusamy.com
	############################################



    def run_YOLO(self):
        print("Running Model")
        blob = cv2.dnn.blobFromImage(self.image, self.image_size[2], (416,416), (0,0,0), True, crop=False)
        self.net.setInput(blob)

        self.outs = self.net.forward(self.get_output_layers(self.net))
        self.set_predictions()
        self.set_bounding_boxes()

    def set_predictions(self):
        print("Set Preds")
        class_ids = []
        confidences = []
        boxes = []


        for out in self.outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * self.image_size[0])# Width)
                    center_y = int(detection[1] * self.image_size[1])#Height)
                    w = int(detection[2] * self.image_size[0])# Width)
                    h = int(detection[3] * self.image_size[1])# Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
                    class_label = str(self.classes[class_id])
                    if(class_label == 'dog'):
                        print("Doggo hit !")
                        self.predictions.append([boxes,confidences,class_ids,class_label])




    def get_predictions(self):
        return self.predictions


    def set_bounding_boxes(self):
        print("Setting BB")
        conf_threshold = 0.5
        nms_threshold = 0.4
        boxes = self.predictions[0][0]

        indices = cv2.dnn.NMSBoxes(self.predictions[0][0], self.predictions[0][1], conf_threshold, nms_threshold)

        boundingBoxes = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            boundingBoxes.append(self.image.copy()[round(y):round(y+h), round(x):round(x+w)])
        self.boundingBoxesPopulated = boundingBoxes

    def show_objects(self):
        print("Showing Object")
        #fig,axes = plt.subplots(nrows = 2, ncols = 4, figsize=(10,10))
        #for ax in axes.flatten():
            #ax.axis('off')
        # TODO: Alter logic to onlly return the image containing a dog, if true & dog>80/90%
        for i,image in enumerate(self.boundingBoxesPopulated):
            classPred  = self.predictions[0][3]


            RGBfix = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #fileName = ("output\\{}{}").format(classPred,i)
            plt.imsave(r'static/staging/segmentation.jpg',RGBfix)
            #axes[0,i].imshow(RGBfix)
            #axes[0,i].set_title( classPred + " " + str(round(self.predictions[1][i],4)*100) + '%' )
            print(self.predictions[0][1])
            return RGBfix,round(self.predictions[0][1][0],4)*100

    @staticmethod
    def get_output_layers(net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers
