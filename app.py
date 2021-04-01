####################################
# Flask Setup
####################################
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
from datetime import datetime
from werkzeug.utils import secure_filename
# import 


app = Flask(__name__)
#app.config["IMAGE_UPLOADS"] = "static/img/uploads/"
app.config["IMAGE_UPLOADS"] = "static/img/uploads/"
path = os.getcwd()

####################################
# Flask Routes
####################################

@app.route("/", methods=["GET", "POST"])
def upload_image():
    message = ""
    if request.method == "POST":
        files = request.files.getlist("image[]")
        print(files)
        if request.files:
            files = request.files.getlist("image[]")
            for image in files:
                print(image.filename)
                mydir = os.path.dirname(__file__)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                print("image saved")
                message = "Number of Total Files: Number of Unique Files: Number of Duplicate Files"
                file_info = similarPhotos()
                total_files = len(file_info[0]) + len(file_info[1])
                unique_files = len(file_info[0])
                duplicates = len(file_info[1])
    return render_template("index.html", message=message) 

@app.route("/getSimilarPhotos")
def similarPhotos():
    data = cluster()
    unique_files = data.keys()
    duplicates = []
    for key in data.keys():
        duplicates.append(len(data[key]))
    print(unique_files)
    print(duplicates)
    return [unique_files, duplicate]

if __name__ == "__main__":
    app.run(debug=True)
