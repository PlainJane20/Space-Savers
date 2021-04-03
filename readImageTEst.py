import requests
import exifread

image_url = "https://static.files-simplefileupload.com/p09tolgo6o18ggnyvux977yg28xy/2013-05-03 17-04-43.JPG"
img_data = requests.get(image_url).content
# 
# print(img_data)

tags = exifread.process_file(img_data)
for tag in tags.keys():
    print(tag, tags[tag])
