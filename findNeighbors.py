import numpy as np
import time
import glob 
import os
import json

from annoy import AnnoyIndex
from scipy import spatial

def cluster():
    start_time = time.time()

    print("--"*10)
    print(f"Step.1 - ANNOY index generation - Started at {time.ctime()}")
    print('--'*10)

    file_index_to_file_name = {}
    file_index_to_file_vector = {}
    file_index_to_product_id = {}

    # config annoy params
    dims = 1792
    n_nearest_neighbors = 20
    trees = 10000

    all_feature_vectors = glob.glob('/Users/lana/DataClass/Space-Savers/Resources/img_vector/*.npz')

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

    named_nearest_neighbors = []
    similar_files = {}

    for i in file_index_to_file_name.keys():
        master_file_name = file_index_to_file_name[i]
        master_vector = file_index_to_file_vector[i]


        nearest_neighbors = t.get_nns_by_item(i, n_nearest_neighbors)
        for j in nearest_neighbors:
            # print(j)
            neighbor_file_name = file_index_to_file_name[j]
            neighbor_file_vector = file_index_to_file_vector[j]

            similarity = 1 - spatial.distance.cosine(master_vector, neighbor_file_vector)

            round_similarity = int((similarity * 10000)) / 10000.0
            # temp_neighboors = []
            if round_similarity >= 0.82:
                named_nearest_neighbors.append( {'similarity': round_similarity, 'master_name': master_file_name, 'neighbor_name': neighbor_file_name})       
            
        print("-"*10)
        print(f'Similarity index: {i}')
        print(f'Master Image file name: {file_index_to_file_name[i]}')
        print(f'Nearest Neighbors: {nearest_neighbors}')
        print(f'{(time.time() - start_time)/60} minuts passed')

        print("Step.2 - Similarity score calculation - Finished")


    
    with open('nearest_neighbors.json', 'w') as out:
        json.dump(named_nearest_neighbors, out)


    print("Step.3 - Data stored in named_nearest_neighbors.json file")

    print(similar_files)
cluster()