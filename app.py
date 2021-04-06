####################################
# Flask Setup
####################################
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# app.config["IMAGE_UPLOADS"] = "static/img/uploads/"
# app.config["IMAGE_UPLOADS"] = "/tmp/"


from findNeighbors import *
from imagePreparation import *
from filesExtraction import *
path = os.getcwd()
# annoy==1.17.0

####################################
# Flask Routes
####################################

@app.route("/", methods=["GET", "POST"])
def upload_image():
    message = ""
    total_files =0
    unique_files =0
    duplicates =0
    if request.method == "POST":
        files = request.files.getlist("image[]")
        print(files)
        if request.files:
            files = request.files.getlist("image[]")
            for image in files:
                print(image.filename)
                mydir = os.path.dirname('static/img/uploads/')
                image.save(os.path.join(mydir, image.filename))
                # image.save(os.path.join("upload", image.filename))
                print("image saved")
                message = "You have: "
    file_info = similarPhotos()
    total_files = len(file_info[0]) + len(file_info[1])
    unique_files = len(file_info[0])
    duplicates = len(file_info[1])
    return render_template("index.html", message=message, total_files=total_files, unique_files=unique_files, duplicates=duplicates) 

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
