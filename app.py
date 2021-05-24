####################################
# Flask Setup
####################################
import os
import imghdr
from flask import Flask, request, redirect, url_for, render_template, abort, jsonify, make_response
from datetime import datetime
from werkzeug.utils import *
# secure_filename

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
            # fileExif = []
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
            for tag in tags:
                if tag == 'Image Make': madeBy = str(tags[tag])
                if tag =='Image Model': model = str(tags[tag])
                if tag =='EXIF DateTimeOriginal':
                    date_and_time = str(tags[tag]).split(' ')
                    date = date_and_time[0]
                    time = date_and_time[1]

                if tag =='MakerNote LensModel': lens = str(tags[tag])

            filesExif.append({'fileID': fileID, 'fileSize': fileSize, 'Image Make': madeBy, 'Image Model': model
                                , 'Image Date': date, 'Image Time': time, 'Lens': lens})
            # save file to current directory
            # file.save(file.filename)
    print(filesExif)
    return jsonify(filesExif)

####################################
# Flask Routes
####################################

# render for index.html 
@app.route("/")
def index_html():
    print("page was loaded")
    return render_template("index.html")

@app.route("/", methods=["POST"])
def file_extraction():

    # # dictionary for all exif info from given files
    # filesExif = []

    if request.method == "POST":
        fileExif()
    #     files = request.files.getlist("image_uploads")
    #     for file in files:
    #         # fileExif = []
    #         fileID = secure_filename(file.filename)
    #         if fileID != '':
    #             fileExt = os.path.splitext(fileID)[1]
    #             if fileExt not in app.config['UPLOAD_EXTENSIONS'] or fileExt != validate_image(file.stream):
    #                 abort(400, "File Extension doesn't supported yet")

            
    #         fileSize = len(file.stream.read())
    #         madeBy = ''
    #         model = ''
    #         date = 0
    #         time = 0
    #         lens = ''

    #         tags = exifread.process_file(file)
    #         for tag in tags:
    #             if tag == 'Image Make': madeBy = str(tags[tag])
    #             if tag =='Image Model': model = str(tags[tag])
    #             if tag =='EXIF DateTimeOriginal':
    #                 date_and_time = str(tags[tag]).split(' ')
    #                 date = date_and_time[0]
    #                 time = date_and_time[1]

    #             if tag =='MakerNote LensModel': lens = str(tags[tag])

    #         filesExif.append({'fileID': fileID, 'fileSize': fileSize, 'Image Make': madeBy, 'Image Model': model
    #                             , 'Image Date': date, 'Image Time': time, 'Lens': lens})
    #         # save file to current directory
    #         # file.save(file.filename)
    #     print(filesExif)
            
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
