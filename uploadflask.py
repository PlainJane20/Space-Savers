import os
from app import app 
from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response
from datetime import datetime

app.config["IMAGE_UPLOADS"] = "img/Uploads":

@app.route("/upload-image", methods=["GET", "POST"]
def upload_image():
    if request.method == "POST":
        if request.files: 
            image = request.files['image']
            image.save(os.path.join(app.config["IMAGE_UPLOADS"]. image.filename))
            print(image saved)
            return redirect(request.url)
    return render_template("Space-Savers/index.html")