from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
import webcolors
from sightengine.client import SightengineClient
import cv2
import numpy as np

class MaskRCNN(object):
    def __init__(self):
        self.net = model_zoo.get_model('mask_rcnn_resnet50_v1b_coco', pretrained=True)
        self.client = SightengineClient('209579874', 'XJbGHACF9jRaLMCijVU5')

    def set_image(self,image_path):
        self.model_data, self.orig_img = data.transforms.presets.rcnn.load_test(image_path)
        self.imageMetaData = self.client.check('properties').set_file(image_path)
        self.imageValues = []
        for row in self.imageMetaData.get("colors").get("other"):
            self.imageValues.append(((row.get('r'),row.get('g'),row.get('b')),((row.get("hex")))))


    def run_model(self):
        print("running model")
        ids, scores, bboxes, masks = [pred[0].asnumpy() for pred in self.net(self.model_data)]
        print("done")
        # paint segmentation mask on images directly
        width, height = self.orig_img.shape[1], self.orig_img.shape[0]
        masks = utils.viz.expand_mask(masks, bboxes, (width, height), scores)
        print("Setting preds")
        self.prediction_info = [ids, scores, bboxes, masks]

    def set_masked_image(self):
        print("Setting masked image")
        self.masked_image = cv2.bitwise_and(self.orig_img.copy(), self.orig_img.copy(), mask = self.prediction_info[3][0,:,:])

    def get_masked_image(self):
        print("returning masked image")
        return self.masked_image

    

    @staticmethod
    def closest_colour(requested_colour):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_colour_name(self,requested_colour):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = self.closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name

    def getImageMetaData(self):
        return self.imageMetaData,self.imageValues

    def getImageChart(self):
        squareIterations = 64

        topX = topY = 0
        bottomX = bottomY = squareIterations

        # Create a black image
        img = np.zeros((512,512,3), np.uint8)
        img.fill(255)

        for colour in self.imageValues:
            cv2.rectangle(img,(topX,topY),(bottomX,bottomY),(colour[0]),-1)
            cv2.putText(img,colour[1], (84,bottomY), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
            cv2.putText(img,(self.get_colour_name(colour[0])[1]), (232,bottomY), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
            #cv2.putText(img,(str(round((colour[1] / pixel_count) * 100,1))), (432,bottomY), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
            topY += squareIterations
            bottomY += squareIterations
        return img
