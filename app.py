####################################
# Flask Setup
####################################
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
<<<<<<< HEAD
#app.config["IMAGE_UPLOADS"] = "static/img/uploads/"
app.config["IMAGE_UPLOADS"] = "/tmp/"
=======
#app.config["IMAGE_UPLOADS"] = "./static/img/uploads/"
app.config["IMAGE_UPLOADS"] = "/tmp/"  
>>>>>>> 86caca7e058e5567adfdfda376a8d7d19db9b014
path = os.getcwd()

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
                mydir = os.path.dirname(__file__)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                print("image saved")
<<<<<<< HEAD
                message = "Number of Total Files: Number of Unique Files: Number of Duplicate Files"
                file_info = similarPhotos()
                total_files = len(file_info[0]) + len(file_info[1])
                unique_files = len(file_info[0])
                duplicates = len(file_info[1])
    return render_template("index.html", message=message, total_files=total_files, unique_files=unique_files, duplicates=duplicates) 

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
=======
                message = "File(s) successfully loaded"
                # image.seek(0)
                # image_string = base64.b64encode(image.read())

                # image_string = image_string.decode('utf-8')
            # return redirect(request.url)
            # image = request.files('image')
            # print(image.filename)
            # image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            # print("image saved")
            # return redirect(request.url)
    return render_template("index.html", message=message)
>>>>>>> 86caca7e058e5567adfdfda376a8d7d19db9b014

if __name__ == "__main__":
    app.run(debug=True)
