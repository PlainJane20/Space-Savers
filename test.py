
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


import json, os
import io





with io.open('/Users/lana/DataClass/SpaceCleaner/Resources/temp_img/296A7765.jpg', 'rb') as file:
    image = Image.open(file)
    exifdata = image.getexif()

    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)     
        print(tag, data)   
        


    