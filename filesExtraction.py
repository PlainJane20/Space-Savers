# from PIL import Image
# from PIL.ExifTags import GPSTAGS, TAGS
import json, os
import exifread

def getDecimalLatLong(lat, longt):
    lat_h = lat[0]
    lat_m = str(lat[1]).split("/")
    lat_min = 0
    if len(lat_m) > 1: lat_min = (float(lat_m[0]) / float(lat_m[1])) / 60
    else: lat_min = float(lat_m[0]) / 60

    lat_s = str(lat[2]).split("/")
    lat_sec = 0
    if len(lat_s) > 1: lat_sec = (float(lat_s[0]) / float(lat_s[1])) / 3600
    else: lat_sec = float(lat[2]) / 3600
    latitude = lat_h + lat_min + lat_sec

    # longt_values = longt.values
    longt_h = longt[0]
    longt_m = str(longt[1]).split("/")
    longt_min = 0
    if len(longt_m) > 1: longt_min = (float(longt_m[0]) / float(longt_m[1])) / 60
    else: longt_min = float(longt_m[0]) / 60

    longt_s = str(longt[2]).split("/")
    longt_sec = 0
    if len(longt_s) > 1: longt_sec = (float(longt_s[0]) / float(longt_s[1])) / 3600
    else: longt_sec = float(longt[2]) / 3600
    longtitude = longt_h + longt_min + longt_sec

    return [latitude, longtitude]  
    
def getFileInfo(path_to_folder):
    # get the list of files in given directory
    
    fileInfo = []
    supported_extensions = ['jpg', 'cr2', 'jpeg']
    
    try: 
        fileList = os.listdir(path_to_folder)
        for file in range(len(fileList)):
            
            split_file_name = os.path.basename(fileList[file]).split('.')

            if split_file_name[-1].lower() in supported_extensions:
                file_id = fileList[file]
                file_path = f"{path_to_folder}/{fileList[file]}"
                file_size = os.path.getsize(f"{path_to_folder}/{fileList[file]}")
                date  = ''
                time = ''
                madeBy = ''
                model = ''
                lens = ''
                lat_ref = ''
                long_ref = ''
                coordinates = []

                with open(file_path, 'rb') as file:
                    tags = exifread.process_file(file)
                    for tag in tags.keys():
                        if tag == 'Image Make': madeBy = str(tags[tag])
                        if tag =='Image Model': model = str(tags[tag])
                        if tag =='EXIF DateTimeOriginal':
                            date_and_time = str(tags[tag]).split(' ')
                            date = date_and_time[0]
                            time = date_and_time[1]

                        if tag =='MakerNote LensModel': lens = str(tags[tag])
                        if tag == "GPS GPSLatitudeRef": lat_ref = str(tags[tag])

                        if tag == "GPS GPSLatitude":
                            lat = tags[tag].values
                            coordinates.append(lat) 

                        if tag == "GPS GPSLongitudeRef": long_ref = str(tags[tag])
                        if tag == "GPS GPSLongitude":
                            longt = tags[tag].values
                            coordinates.append(longt)
                        
                decimal_coordinates = []   
                if len(coordinates) != 0:
                    decimal_coordinates = getDecimalLatLong(coordinates[0], coordinates[1])
                    if lat_ref != 'N': decimal_coordinates[0] = float(f'-{decimal_coordinates[0]}')
                    if long_ref != 'E': decimal_coordinates[1] = float(f'-{decimal_coordinates[1]}')

                fileInfo.append({"file_id": file_id, "file_path": file_path, "file_bytes_size": file_size
                                , "Date": date, "Time": time, "lensType": lens
                                , 'madeBy': madeBy, 'model': model, 'coordinates': decimal_coordinates})
        return fileInfo
        
    except FileNotFoundError:
        return "Folder not found"


# SHOUKD BE MOVED TO APP.PY
def getUserpath(path_to_folder):
    if os.path.exists("filesInfo.json"):
        os.remove("filesInfo.json")
    
    with open('filesInfo.json', 'w') as out:
        json.dump(getFileInfo(path_to_folder), out)


# getUserpath("/Users/lana/Desktop/PhotoForProject/jpg")