####################################
# Flask Setup
####################################
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
from datetime import datetime
from werkzeug.utils import secure_filename
# import 


app = Flask(__name__)
#app.config["IMAGE_UPLOADS"] = "./static/img/uploads/"
app.config["IMAGE_UPLOADS"] = "/tmp/"  
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

if __name__ == "__main__":
    app.run(debug=True)
