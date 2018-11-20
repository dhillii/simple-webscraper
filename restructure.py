import json
from pprint import pprint
from string import digits

with open('curl-iq-final.json', encoding="utf8") as f:
    data = json.load(f)

database = {
        'hair_types':{
            '4A':{'products':{}},
            '4B':{'products':{}},
            '4C':{'products':{}},
            '3A':{'products':{}},
            '3B':{'products':{}},
            '3C':{'products':{}},
            '2A':{'products':{}},
            '2B':{'products':{}},
            '2C':{'products':{}}
        }
    }

for key in data['hair_types']:

    prod_list = data['hair_types'][key]['products']

    for prod_obj in prod_list:
        try:
            pkey = list(prod_obj.keys())
            pkey = pkey[0]
            pkey = pkey.replace("(", "")
            pkey = pkey.replace(")", "")
            pkey = pkey.replace("oz.", "")
            pkey = pkey.replace("oz", "")
            pkey = pkey.replace(".", "")
            remove_digits = str.maketrans('', '', digits)
            pkey = pkey.translate(remove_digits)
            pkey=pkey.rstrip()
            
        

            value = list(prod_obj.values())
            value = value[0]
            

            database['hair_types'][key]['products'][pkey] = value
        except:
            pass

print(database)

with open('curl-iq-v2.json', 'w') as file:
                json.dump(database, file)


