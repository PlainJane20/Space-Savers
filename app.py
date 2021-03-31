####################################
# Flask Setup
####################################
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
from datetime import datetime
from werkzeug.utils import secure_filename
# import 

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "static/img/uploads/"

path = os.getcwd()

####################################
# Flask Routes
####################################

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        files = request.files.getlist("image[]")
        print(files)
        if request.files:
            files = request.files.getlist("image[]")
            for image in files:
                print(image.filename)
                mydir = os.path.dirname(__file__)
                image.save(os.path.join(mydir + "/" + app.config["IMAGE_UPLOADS"], image.filename))
                print("image saved")
            return redirect(request.url)
            # image = request.files('image')
            # print(image.filename)
            # image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            # print("image saved")
            # return redirect(request.url)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
