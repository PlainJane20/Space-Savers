from PIL import Image
from PIL.ExifTags import TAGS
import json, os

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
                date_and_time  = ''
                madeBy = ''
                model = ''
                with open(file_path, 'rb') as file:
                    image = Image.open(file)
                    exifdata = image.getexif()

                    for tag_id in exifdata:
                        tag = TAGS.get(tag_id, tag_id)
                        data = exifdata.get(tag_id)
                        if isinstance(data, bytes): data = data.decode()              
                        if tag == 'DateTimeOriginal': date_and_time = data                        
                        if tag == "Make": madeBy = data
                        if tag == 'Model': model = data


                fileInfo.append({"file_id": file_id, "file_path": file_path, "file_bytes_size": file_size
                                , "Date": date_and_time, 'madeBy': madeBy, 'model': model})
        return fileInfo
        
    except FileNotFoundError:
        return "Folder not found"
    except UnicodeDecodeError:
        return "'utf-8' codec can't decode byte 0xf4 in position 39: invalid continuation byte"

    


print(getFileInfo("/Users/lana/DataClass/SpaceCleaner/Resources/img"))



# [{file_id: file_name, file_path: path_to_file, file_size: size, file_extension: jpg/png},
# {file_id: file_name, file_path: path_to_file, file_size: size, file_extension: jpg/png},
# {file_id: file_name, file_path: path_to_file, file_size: size, file_extension: jpg/png}]