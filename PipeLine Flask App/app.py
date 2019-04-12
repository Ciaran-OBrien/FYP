from flask import Flask, redirect,request, render_template,url_for, send_from_directory, request, make_response, send_file
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import logging, os, cv2
from werkzeug import secure_filename
from flask_dropzone import Dropzone

import sys
import io, base64
from io import BytesIO
from skimage.io import imsave

from modules.fileup import FileUp
from modules.yolo import YOLO
from modules.resnet50 import ResNet50

#from modules.maskrcnn import MaskRCNN
#from modules.database import Dogs
from modules.enum import Size, Status


basedir = os.path.abspath(os.path.dirname(__file__))
file_path = basedir + "\\database.db"



app = Flask(__name__)
Bootstrap(app)
dropzone = Dropzone(app)
fileUpCheck = FileUp()
yolo = YOLO()
resnet50 = ResNet50()
#maskrcnn = MaskRCNN()




app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'static\\uploads\\staging'),
    UPLOADED_PATH_ =os.path.join('static\\uploads\\staging'),
    LOST_PATH=os.path.join('static\\uploads\\lost'),
    FOUND_PATH=os.path.join('static\\uploads\\found'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

db = SQLAlchemy(app)

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    fileLocation = ""
    if request.method == 'POST':
        if (fileUpCheck.get_check() == False):
            f = request.files.get('file')
            f.save(os.path.join(app.config['UPLOADED_PATH_'], f.filename))
            fileUpCheck.set_check(True)
            fileUpCheck.set_filePath(str(os.path.join(app.config['UPLOADED_PATH_'])))
            fileUpCheck.set_fileName(f.filename)

        else:
            result = request.form
            option = request.form['Radios']
            text = request.form['inputDogName']
            status = request.form['options']

            if status == 'lost':
                fileLocation = str(os.path.join(app.config['LOST_PATH'],fileUpCheck.get_fileName()))

                os.rename(fileUpCheck.get_filePath() +"\\"+ fileUpCheck.get_fileName(), fileLocation)
            elif status == 'found':
                fileLocation = str(os.path.join(app.config['FOUND_PATH'],fileUpCheck.get_fileName()))
                os.rename(fileUpCheck.get_filePath() +"\\"+ fileUpCheck.get_fileName(), fileLocation)

            newDog = Dogs(name = request.form['inputDogName'],
            fileLocation = fileLocation,
             breed = "Beauceron ",
             colours = "Black,Brown",
             size = Size.from_str(request.form['Radios']),
             status = request.form['options'],
             location = request.form['inputArea'])

            db.session.add(newDog)
            db.session.commit()
            fileUpCheck.set_filePath(fileLocation)
            fileUpCheck.set_check(False)
            return redirect(url_for('scan'))
    return render_template('upload.html',title="Upload Dog Image",img = 'size_chart.png')

# @app.route('/colours')
# def colours():
#     maskrcnn.set_image('static/masked.png')
#     # maskrcnn.run_model()
#     # maskrcnn.set_masked_image()
#
#     strIO = BytesIO()
#     imsave(strIO,maskrcnn.getImageChart(), plugin='pil', format_str='png')
#     strIO.seek(0)
#     return send_file(strIO, mimetype='image/png')

# @app.route('/predict')
# def predict():
#
    # resnet50.run_model(get_image()[0])
    # return render_template('prediction.html',img = 'uploads/staging/Belgian_sheepdog_01485.jpg',predictions = resnet50.get_predictions() )

@app.route('/scan/')
def scan():
    image_path_to_scan = fileUpCheck.get_filePath()
    yolo.set_image(image_path_to_scan)
    yolo.run_YOLO()


    #strIO = BytesIO()
    #imsave(strIO, yolo.show_objects()[0], plugin='pil', format_str='png')
    #strIO.seek(0)
    #cv2.imwrite('static//staging//segmentation.jpg',yolo.show_objects()[0])
    # response = send_file(strIO, mimetype='image/jpg')
    # output = io.BytesIO()
    # yolo.show_objects()[0].convert('RGBA').save(output, format='PNG')
    # output.seek(0, 0)


    resnet50.run_model(image_path_to_scan)
    classification = resnet50.get_predictions()

    #return redirect(url_for('upload'))
    return render_template('prediction.html',prediction=round(yolo.get_predictions()[0][1][0],4)*100, classes = classification)

    #return send_file(strIO, mimetype='image/png')


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=TestClass.fxn(), users = TestClass.getUsers())


# Setup Homepage Route
@app.route('/')
def index():
    deleted_objects = Dogs.__table__.delete()
    db.session.execute(deleted_objects)
    db.session.commit()
    return render_template('index.html',title="Home Page")

@app.route('/lostfound')
def lostfound():
    #db.session.query(Dogs).delete()
    # testDogs = [
    #     Dogs(name = "Rolo", fileLocation="static/uploads/found/Beauceron_01284.jpg", breed = "Beauceron ", colours = "Black,Brown", size = Size.three, status = Status.found,location = "Kimmage"),
    #     Dogs(name = "Ziggy", fileLocation="static/uploads/found/Labrador_retriever_06466.jpg",breed = "Labrador", colours = "Black", size = Size.four, status = Status.found,location = "Old Bawn"),
    #     Dogs(name = "Robbie", fileLocation="static/uploads/found/Beagle_01141.jpg",breed = "Beagle", colours = "Cream, White, Brown", size = Size.one, status = Status.found,location = "N/A"),
    #     Dogs(name = "Bobby", fileLocation="static/uploads/found/Collie_03794.jpg",breed = "Collie", colours = "Black, Grey, White", size = Size.one, status = Status.found,location = "N/A"),
    #     Dogs(name = "Fido", fileLocation="static/uploads/lost/Great_dane_05322.jpg",breed = "Great Dane", colours = "Brown, Olive", size = Size.two, status = Status.lost,location = "Firhouse"),
    #     Dogs(name = "Mr Ruffles", fileLocation="static/uploads/lost/Mastiff_06827.jpg",breed = "Mastiff", colours = "Brown, White", size = Size.one, status = Status.lost,location = "Clontarf"),
    #     Dogs(name = "Lassie", fileLocation="static/uploads/lost/Collie_03849.jpg",breed = "Collie ", colours = "White, Brown, Cream", size = Size.three, status = Status.lost,location = "Florida"),
    #     Dogs(name = "Lucy", fileLocation="static/uploads/found/Airedale_terrier_00175.jpg",breed = "Airedale Terrier", colours = "Brown, Orange", size = Size.four, status = Status.found,location = "Dundrum"),
    #     Dogs(name = "Bella", fileLocation="static/uploads/lost/Irish_water_spaniel_05983.jpg",breed = "Irish Water Spaniel", colours = "Brown, Olive", size = Size.five, status = Status.lost,location = "Terrenure"),
    #     Dogs(name = "Puppy Goo-Goo", fileLocation="static/uploads/lost/Saint_bernard_08020.jpg",breed = "Saint Bernard", colours = "White, Brown", size = Size.one, status = Status.lost,location = "Springfield")
    # ]
    # db.session.bulk_save_objects(testDogs)
    # db.session.commit()
    lostQuery  = Dogs.query.filter_by(status='lost').all()
    foundQuery  = Dogs.query.filter_by(status='found').all()
    return render_template(
    'lostfound.html',
    title="Lost and Found",
    lost = lostQuery,
    found = foundQuery)

def get_image():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(app.config['UPLOADED_PATH']):
        f.extend(filenames)
        break
    image_info = os.path.join(app.config['UPLOADED_PATH'],f[0])
    return image_info

from modules.enum import Size, Status

class Dogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileLocation = db.Column(db.String(20), unique=False, nullable=False, default='static/uploads/dog_image_default.jpg')
    name = db.Column(db.String(20), unique=False, nullable=True)
    breed = db.Column(db.String(120), unique=False, nullable=True)
    colours = db.Column(db.String(120), unique=False, nullable=True)
    size = db.Column(db.Enum(Size), unique=False, nullable=False)
    extras = db.Column(db.String(120), unique=False, nullable=True)
    status = db.Column(db.Enum(Status),unique=False, nullable=False)
    location = db.Column(db.String(120),unique=False, nullable=True)



class TestClass(object):
    @staticmethod
    def fxn():
        testString = "Preds"
        return testString

    @staticmethod
    def getUsers():
        return ["qwe","we","aasd"]



if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000, debug=True)
    db.session.query(Dogs).delete()
