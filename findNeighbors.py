import numpy as np
import time
import glob 
import os
import json
from config import *

from annoy import AnnoyIndex
from scipy import spatial

def checkValue(value, dic):
    response = False
    for key in dic.keys():
        values = dic[key]
        if value not in values:
            print(f"Value not found: {value}")
            response = False
        else:
            print(f"Value found: {value}")
            response = True
            break
    return response

def cluster():
    start_time = time.time()

    print("--"*10)
    print(f"Step.1 - ANNOY index generation - Started at {time.ctime()}")
    print('--'*10)

    file_index_to_file_name = {}
    file_index_to_file_vector = {}
    # file_index_to_product_id = {}

    # config annoy params
    dims = 1792
    n_nearest_neighbors = 20
    trees = 10000

    all_feature_vectors = glob.glob('static/img/img_vectors/*.npz')

    t = AnnoyIndex(dims, metric='angular')

    for file_index, i in enumerate(all_feature_vectors):
        file_vector = np.loadtxt(i)

        file_name = os.path.basename(i).split('.')[0]
        file_index_to_file_name[file_index] = file_name
        file_index_to_file_vector[file_index] = file_vector

        t.add_item(file_index, file_vector)

        print('-'*10)
        print(f"Annoy index: {file_index}")
        print(f"Image file name: {file_name}")
        print(f"{(time.time() - start_time)/60} minuts passed")

    t.build(trees)

    print("Step.1 ANNOY INDEX generation -Finished")
    print("Step.2 - Similarity score calculation - Started")

    
    similar_files = {}

    for i in file_index_to_file_name.keys():
        
        master_file_name = file_index_to_file_name[i]
        master_vector = file_index_to_file_vector[i]
        if master_file_name in similar_files.keys():
            print(f" IN DIC KEY: Master file: {master_file_name} and i= {i} PASSED")
            continue
        else:
            if checkValue(master_file_name, similar_files) == True:
                print(f"Continue: checkValue = {checkValue(master_file_name, similar_files)}")
                print(f" IN DIC LIST Master file: {master_file_name} and i= {i} PASSED")
                continue
            else:
                print(f"ELSE: checkValue = {checkValue(master_file_name, similar_files)}")
                similar_files[master_file_name] = []
                nearest_neighbors = t.get_nns_by_item(i, n_nearest_neighbors)

                for j in nearest_neighbors:
                    print(f"        NESTED LOOP Iteration # {j}")
                    neighbor_file_name = file_index_to_file_name[j]
                    neighbor_file_vector = file_index_to_file_vector[j]

                    print(f"        NEIGBOR NAME IS {neighbor_file_name}")

                    similarity = 1 - spatial.distance.cosine(master_vector, neighbor_file_vector)
                    round_similarity = int((similarity * 10000)) / 10000.0
            
            
                    if round_similarity >= 0.85 and neighbor_file_name != master_file_name :
                        similar_files[master_file_name].append(neighbor_file_name)

        print(f"END: MASTER FILE is {master_file_name}, SIMILAR FILE: {similar_files}")
        print("Step.2 - Similarity score calculation - Finished")

    with open("static/json/similarPhoto.json", 'w') as out:
        json.dump(similar_files, out)
    print("Step.3 - Data stored in similarPhoto.json file")
    return similar_files
    