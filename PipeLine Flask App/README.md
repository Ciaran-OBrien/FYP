# FindMyDogg
## Exploring Machine Learing Techniques to Identify Dogs.

We see lost pets everywhere, and its heart breaking, ever more so to the owners of these pets. Be it through neglect, or a stray pet, it can be difficult to retrieve them.

With dogs, we're advised to not approach them, rather, call a vet, and they'll process the dog. However, all this is timely, costly and often ineffective method of identifying the lost dog when there's no microchip present. 

This project proposes building a time saving, cost effective, and safer method, for the public to use. The project explores machine learning and image processing techniques to detect, classify and obtain abstract features about a dog. There is room for future research looking towards identifying the dog itself. 

Digital Ocean hosts the application and built using Python, and web application framework Flask. Tensorflow functions as the back-end for the majority of machine learning aspects.  The project also makes use of the Keras API to incorporate powerful Neural Networks.


### Prerequisites

Only a few prerequisites in order to follow the steps below.

```
Python3
Pip Installs Packages(PIP)
```


## Getting Started
Firstly, a demo of the application is hosted here: [findmydoggo.co.uk](http://findmydoggo.co.uk) Funny that .co.uk domain name was free ??

Otherwise if you wish to run this project on your own machine and deploy on your local host server follow these instructions:
* See previous heading Prerequisites for manditory programs that should already be installed on your machine
* Run the following command:
``` 
git clone https://github.com/Ciaran-OBrien/FYP
```
* Navigate to the Flask App folder
* Run the following command:
```
pip install -r requirements.txt
```
* Once everything is installed succesfully, run the following to start the webapp
```
flask run
```

* Point your web browser to the promted webserver address: [127.0.0.1:5000](127.0.0.1:5000)

## Sample Usage Steps

* Open the loading page, either through your local host machine or through the website.
* Move to the Scan Dog Page
* Drag & Drop an image, or click & load form file explorer
* Fill in the form details
* Click Register Dog and wait for results
* Head over to Lost and Found page, and you'll see your uploaded dog

*Note: Web-App is a proof-of-concept. Any function & information shown on the Lost and Found page is purely developmental*

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - A Microframework
* [Python](https://docs.python.org/3/) - Programming language of choice
* [OpenCV](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html) - Image Processing Library
* [DarkNet](https://pjreddie.com/darknet/yolo/) - Open source neural network framework providing YOLOv3 Network 
* [Keras](https://keras.io) - Deep Learling Library providing ResNet50 Network
* [Gluon-CV](https://gluon-cv.mxnet.io/api/index.html) - Deep Learning Toolkit providing the Mask R-CNN Network

## Authors

* **Ciarán O'Brien** - *Initial work* - [Git Profile](https://github.com/Ciaran-OBrien)
* **Dr. John Gilligan** - *First Reader*
* **Prof. Dr.Bernhard Humm** - *Second Reader*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
In the process of this dissertation, I was fortunate to obtain the assistance of many people, whom I would like to present my genuine thanks. My appreciation goes first to my supervisor, Dr. John Gilligan. His guidance and attention to detail ensured that I and the project both stayed on track

My next appreciation goes to my second supervisor, Prof. Dr. Bernhard G. Humm. My work with Humm is a part of the EDDIT programme, a dual degree from Technological University of Dublin, and Hochschule Darmstadt.

The project gained extra assistance from many different lectures, and in part would not be possible without the support from all the staff and lectures at TUD.
Finally, I would also like to thank my family for all their encouragement and assistance during this project. 


##### YOLOv3 Implementation

################################

Object detection - YOLO - OpenCV

Author : Arun Ponnusamy   (July 16, 2018)

Website : http://www.arunponnusamy.com

################################

##### Original Inspiration
Past Student - Damien Glynn - Cheers!
