####################################
# Flask Setup
####################################
import os
import imghdr
from flask import Flask, request, redirect, url_for, render_template, abort, jsonify, make_response
from datetime import datetime
from werkzeug.utils import *

import PIL
import PIL.Image
from io import BytesIO
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np 

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'


app = Flask(__name__)

# app.config["IMAGE_UPLOADS"] = "static/img/uploads/"
# app.config["IMAGE_UPLOADS"] = "/tmp/"

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.JPG', '.jpeg', '.JPEG']

from findNeighbors import *
from imagePreparation import *
from filesExtraction import *
path = os.getcwd()
# annoy==1.17.0

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    print('VALIDATE IMAGE', format)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg' )
    
def fileExif():
    # dictionary for all exif info from given files
    filesExif = []

    if request.method == "POST":
        files = request.files.getlist("image_uploads")
        
        for file in files:
            fileID = secure_filename(file.filename)
            if fileID != '':
                fileExt = os.path.splitext(fileID)[1]
                if fileExt not in app.config['UPLOAD_EXTENSIONS'] or fileExt != validate_image(file.stream):
                    abort(400, "File Extension doesn't supported yet")

            
            fileSize = len(file.stream.read())
            madeBy = ''
            model = ''
            date = 0
            time = 0
            lens = ''

            tags = exifread.process_file(file)
            print("Tags were gotten")
            for tag in tags:
                if tag == 'Image Make': madeBy = str(tags[tag])
                if tag =='Image Model': model = str(tags[tag])
                if tag =='EXIF DateTimeOriginal':
                    date_and_time = str(tags[tag]).split(' ')
                    date = date_and_time[0]
                    time = date_and_time[1]

                if tag =='MakerNote LensModel': lens = str(tags[tag])
            print('LOOP TAG ended')

            filesExif.append({'fileID': fileID, 'fileSize': fileSize, 'Image Make': madeBy, 'Image Model': model
                                , 'Image Date': date, 'Image Time': time, 'Lens': lens})
    
    return filesExif

def imgPreparation(file):
    # Prepare image to convert it to image vector           
    img = PIL.Image.open(file)
    img = np.array(img)
    img = tf.image.resize_with_pad(img, 224, 224)
    img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    print('img is ready')
    # create image vectors
    module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/5"
    print("MODEL TO HANDLE", module_handle)
    # module = hub.load(module_handle)
    module = hub.load(module_handle)

    print("MODULE is loaded")
    features = module(img)
    print("FEATIRES", features)
    feature_set = np.squeeze(features)
    print('VECTOR', feature_set)

    return feature_set


def saveExifDataToJson(list, file_name):
    file_path = f'static/json/{file_name}.json'
    if os.path.exists(file_path):
        os.remove(file_path)
    
    with open(file_path, 'w') as out:
        json.dump(list, out)

####################################
# Flask Routes
####################################

# render for index.html 
@app.route("/")
def index_html():
    print("page was loaded")
    return render_template("index.html")

@app.route("/", methods=["POST"])
def file_choosing():

    if request.method == "POST":
        filesExif = fileExif()
        userExifFile = 'userExifFile'
        saveExifDataToJson(filesExif, userExifFile)
    return redirect(url_for('index_html'))



@app.route('/travelMap')
def travelMAp():
    return render_template('travelMap.html')

@app.route('/about')
def aboutUS():
    return render_template("aboutus.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route("/getSimilarPhotos")
def similarPhotos():
    get_image_feature_vectors()
    
    data = cluster()
    unique_files = data.keys()
    duplicates = []
    for key in data.keys():
        duplicates.append(len(data[key]))
    print(unique_files)
    print(duplicates)
    return [unique_files, duplicates]

@app.route("/getDuplicateSize")
def getDuplicateSize():
    similar_photos = similarPhotos()
    photo_info = getFileInfo('static/img/uploads/')

    size_of_duplicates_files = 0

    for key in similar_photos.keys():      
        for i in range(len(photo_info)):        
            for file in similar_photos[key]:
                list_of_duplicates = photo_info[i]['file_id'].split(".")[0]
                if file in list_of_duplicates:
                    size_of_duplicates_files += photo_info[i]['file_bytes_size']
    return size_of_duplicates_files

@app.route("/getUniqueSize")
def getUniqueSize():
    similar_photos = similarPhotos()
    photo_info = getFileInfo('static/img/uploads/')
    size_of_unique_files = 0
    for key in similar_photos.keys():      
        for i in range(len(photo_info)):        
            file = photo_info[i]['file_id'].split(".")[0]
            if key == file:
                size_of_unique_files += photo_info[i]['file_bytes_size']
    return size_of_unique_files

if __name__ == "__main__":
    app.run(debug=True)
