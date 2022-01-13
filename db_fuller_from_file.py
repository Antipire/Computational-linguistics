import mysql
import mysql.connector
from bs4 import BeautifulSoup
import requests as req
import time


def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "REMOVED"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['news_data']


dbname = get_database()
f = open("links.txt", "r")
for line in f:
    link = f.readline()
    print(f"https://v102.ru{link[:-1]}")

    resp = req.get(f"https://v102.ru{link[:-1]}")
    soup = BeautifulSoup(resp.text, 'lxml')

    # Get article headline
    article = soup.find("h1", {'itemprop': "headline"})

    # Get news publishing date
    date = soup.find("span", class_="date-new")

    # Get news text
    news = soup.find_all("div", class_="n-text")
    news_text = news[0].text

    # Get comments number
    comments = soup.find("span", class_="attr-comment")

    news_dict = {'link': link, 'article': article.text, 'date': date.text, 'text': news_text,
                 'comments': comments.text}

    dbname['news_collection'].insert_one(news_dict)

    time.sleep(1.5)
