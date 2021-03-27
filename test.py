
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


import json, os
import io





with io.open('/Users/lana/DataClass/SpaceCleaner/Resources/temp_img/IMG_0004.jpg', 'rb') as file:
    image = Image.open(file)
    exifdata = image.getexif()

    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)     
        if tag == 'DateTimeOriginal': 
            date_and_time = data .split(" ")       
            print('-'*20)
            print(date_and_time)   
        


    