from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
import json, os
import io


def getLatLong(path_to_file):
    latitude = ""
    longtitude = ""
    with io.open(path_to_file, 'rb') as file:
        image = Image.open(file)
        exifdata = image.getexif()

        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)     

            if tag == 'GPSInfo':
                for key in data.keys():
                    name = GPSTAGS.get(key, key)
                
                    if name == 'GPSLatitudeRef':
                        lat_ref = data.get(key)
                    if name == 'GPSLatitude':
                        lat = data.get(key)
                        lat = float(lat[0] + (lat[1] / 60) + (lat[2] / 3600))
                        if lat_ref == 'N': latitude = f'{lat}'
                        else: latitude = f'-{lat}'
                        
                    if name == 'GPSLongitudeRef':
                        long_ref = data.get(key)
                    if name == 'GPSLongitude':
                        longt = data.get(key)
                        longt = float(longt[0] + (longt[1] / 60) + (longt[2] / 3600))
                        if long_ref == "E": longtitude = f'{longt}'
                        else: longtitude = f'-{longt}'

    return([latitude, longtitude])
    
    
def getFileInfo(path_to_folder):
    # get the list of files in given directory
    
    fileInfo = []
    
    try: 
        fileList = os.listdir(path_to_folder)
        for file in range(len(fileList)):
            
            split_file_name = os.path.basename(fileList[file]).split('.')
            print(split_file_name)
            
            if split_file_name[-1] == 'jpg':
                file_id = fileList[file]
                file_path = f"{path_to_folder}/{fileList[file]}"
                file_size = os.path.getsize(f"{path_to_folder}/{fileList[file]}")
                date  = ''
                time = ''
                madeBy = ''
                model = ''
                lens = ''
                coordinates = []

                with io.open(file_path, 'rb') as file:
                    image = Image.open(file)
                    exifdata = image.getexif()

                    for tag_id in exifdata:
                        tag = TAGS.get(tag_id, tag_id)
                        data = exifdata.get(tag_id)              
                        if tag == 'DateTimeOriginal': 
                            date_and_time = data .split(" ")         
                            date = date_and_time[0]
                            time = date_and_time[1]
                                           
                        if tag == "Make": madeBy = data
                        if tag == 'Model': model = data
                        if tag == 'LensModel': lens = data
                        if tag == "GPSInfo": coordinates = getLatLong(file_path)


                fileInfo.append({"file_id": file_id, "file_path": file_path, "file_bytes_size": file_size
                                , "Date": date, "Time": time
                                , 'madeBy': madeBy, 'model': model, 'coordinates': coordinates})
        return fileInfo
        
    except FileNotFoundError:
        return "Folder not found"


# SHOUKD BE MOVED TO APP>PY
def getUserpath(path_to_folder):
    if os.path.exists("filesInfo.json"):
        os.remove("filesInfo.json")
    
    with open('filesInfo.json', 'w') as out:
        json.dump(getFileInfo(path_to_folder), out)


getUserpath("/Users/lana/DataClass/SpaceCleaner/Resources/temp_img")