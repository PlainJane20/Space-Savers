import json

perfect_output = {}

with open('nearest_neighbors.json', 'r') as f:   
    data = json.load(f) 
    # print(data)
    perfect_output[data[0]['master_name']] = [data[0]['neighbor_name']]
    print(perfect_output)
    for i in range(len(data)):
        print('-'*20)
        print(f'{i, data[i]}')
        if data[i]['master_name'] in perfect_output.keys() and data[i]['neighbor_name'] != data[i]['master_name']:
            print(f"FILE {data[i]['master_name']} IN PERFECT OUTPUT")
            if data[i]['neighbor_name'] not in perfect_output[data[i]['master_name']]:
                perfect_output[data[i]['master_name']].append(data[i]['neighbor_name'])
                print('OUTPUT IS', perfect_output)

        if data[i]['master_name'] not in perfect_output.keys() and data[i]['neighbor_name'] != data[i]['master_name']:
            for key in perfect_output.keys():
                if data[i]['master_name'] not in perfect_output[key]:
                    perfect_output[data[i]['master_name']] = [data[i]['neighbor_name']] 
        
        

        print('&'*20)

print(perfect_output)
print('-'*10)
# print(perfect_output['2013-09-28 19-34-43'])
print(len(perfect_output.keys()))

print(len(perfect_output.values()))
    