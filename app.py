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

def getUserpath(path_to_folder):
    if os.path.exists("filesInfo.json"):
        os.remove("filesInfo.json")
    
    with open('filesInfo.json', 'w') as out:
        json.dump(getFileInfo(path_to_folder), out)

if __name__ == "__main__":
    app.run(debug=True)




getUserpath("/Users/lana/DataClass/SpaceCleaner/Resources/temp_img")