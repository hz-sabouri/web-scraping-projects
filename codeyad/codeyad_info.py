import requests
import csv

csv_title = ["Title","time","price","category"]
url = 'https://api.codeyad.com/api/course/getByFilter'
items = []

for j in range(1,4):
    params= {
        'pageId': j,
        'take' : 12
    }

    response = requests.get(url,params=params)
    datajson = response.json()
    for item in datajson['data']['data']:
        myitem={
            "Title": item["courseTitle"],
            "time": item["duration"],
            "price": item["price"],
            "category" : item["categoryTitle"]
        }
        items.append(myitem)

with open('codeyad_info.csv','a',encoding='utf8',newline='') as codeyadcorse:
    writer = csv.DictWriter(codeyadcorse,fieldnames=csv_title)
    writer.writeheader()
    for i in items:
        writer.writerow(i)
