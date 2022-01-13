import time

from pymongo import MongoClient
import os

os.chdir('/home/zuga/Desktop/tomita-parser/build/bin')
client = MongoClient("mongodb+srv://DB_NEWS_DATA:1234@cluster0.wshon.mongodb.net/news_data")
database = client["news_data"]
collection = database["news_collection"]
a=1
words =[]
for news in collection.find( {} ):
    with open("input.txt","w") as f:
        print(news['text'])
        f.write(news['text'])

    f.close()
    os.system("./tomita-parser config.proto")
    person = []
    object = []

    with open("facts.txt", "r") as f2:
        foutput = f2.read()
        words = foutput.split()
        for i in range(len(words)):

            if words[i] == "Name":
                if words[i + 2] not in person:
                    person.append(words[i + 2])
            elif words[i] == "Thing":
                place = ""
                while words[i + 2] != "}":
                    place += " " + words[i + 2]
                    i += 1
                if place not in object:
                    object.append(place)
    f2.close()


    for i in range(len(person)):
        collection.update_one({
            "_id": news["_id"]
        }, {
            "$set": {
                "Person": person[i]
            }
        })

    for i in range(len(object)):
        collection.update_one({
            "_id": news["_id"]
        }, {
            "$set": {
                "Object": object[i]
            }
        })

    person.clear()
    object.clear()

    a+=1
    print(a)




