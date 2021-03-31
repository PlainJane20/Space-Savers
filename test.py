import json

# perfect_output = {}

# with open('nearest_neighbors.json', 'r') as f:   
#     data = json.load(f) 
#     # print(data)
#     # perfect_output[data[0]['master_name']] = [data[0]['neighbor_name']]
#     # print(perfect_output)

#     for i in range(len(data)):
#         print('-'*20)
#         print(f'{i, data[i]}')

#         if data[i]['master_name'] in perfect_output.keys(): 
#         # and data[i]['neighbor_name'] != data[i]['master_name']:
#             print(f"FILE {data[i]['master_name']} IN PERFECT OUTPUT")
#             if data[i]['neighbor_name'] not in perfect_output[data[i]['master_name']]:
#                 print('FileNAme was add as neighbor')
#                 perfect_output[data[i]['master_name']].append(data[i]['neighbor_name'])
#                 # print('OUTPUT IS', perfect_output)

#         if data[i]['master_name'] not in perfect_output.keys():
#             print(f"FILE {data[i]['master_name']} NOT IN PERFECT OUTPUT")
#         #  and data[i]['neighbor_name'] != data[i]['master_name']:
#             if len(perfect_output.keys()) == 0:
#                 perfect_output[data[i]['master_name']] = [data[i]['neighbor_name']] 
#             else:
#                 for key in list(perfect_output.keys()):
#                     if data[i]['master_name'] not in perfect_output[key]:
#                         perfect_output[data[i]['master_name']] = [data[i]['neighbor_name']] 
                

        

#         print('&'*20)

# print(perfect_output)
# print('-'*10)
# # print(perfect_output['2013-09-28 19-34-43'])
# print(len(perfect_output.keys()))

# print(len(perfect_output.values()))
word_freq = {'is': [1, 3, 4, 8, 10],
            #  'at': [3, 10, 15, 7, 9],
            #  'test': [5, 3, 7, 8, 1],
            #  'this': [2, 3, 5, 6, 11],
             'why': [10, 3, 9, 8, 12]
             }
# Check if a value exist in dictionary with multiple value
# value = 10
print(word_freq.items())

# Get list of keys that contains the given value
# list_of_keys = [key
#                 for key, list_of_values in word_freq.items()
#                 if value in list_of_values]
# if list_of_keys:
#     print(list_of_keys)
# else:
#     print('Value does not exist in the dictionary')
# print('*'*10)

    
def checkValue(value, dic):
    response = True
    print(f"dic.keys {dic.keys()}")
    for key in dic.keys():
        print(f"key {key}")
        values = dic[key]
        print(f"values = {values}")
        print(f"values type = {type(values)}")
        if value not in values:
            response = False
        else:
            response = True
    return response
# print(checkValue(3, word_freq))
# print(word_freq.items())

d = {'IMG_0005': ['IMG_0005', 'IMG_0006', 'IMG_0004_copy', 'IMG_0004']
    , 'PXL_20210314_020726755': ['PXL_20210314_020726755', 'PXL_20210314_020732248', 'PXL_20210314_020719504']
    , 'IMG_0033': ['IMG_0033', 'IMG_0035', 'IMG_0034', 'IMG_0032', 'IMG_0031', 'IMG_0030']}

print(checkValue('IMG_0032', d))