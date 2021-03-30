from filesExtraction import getFileInfo
from flask import Flask, render_template, redirect, jsonify
from flask.json import tojson_filter
from PIL import Image
from PIL.ExifTags import TAGS
import json, os

app = Flask(__name__)

@app.route("/")
def home():
    
    
    return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)




