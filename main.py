from bs4 import BeautifulSoup
import requests as req
from queue import Queue
from threading import Thread, Event, current_thread
from pymongo import MongoClient
import pymongo


def crawler(wait_time: int, event_crawler: Event, links: Queue):
    while True:
        resp = req.get(f"https://v102.ru/center_line_dorabotka_ajax.php?page=0&category=0")
        soup = BeautifulSoup(resp.text, 'lxml')
        page_links = []
        for a in soup.find_all("a", class_="detail-link-text", href=True):
            page_links.append(a['href'])
        links.put(page_links)
        parse_news_data(page_links)
        event_crawler.wait(wait_time)


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://DB_NEWS_DATA:1234@cluster0.wshon.mongodb.net/news_data"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['news_data']


# Pushing data to DB
# link, article, date, text, comments
def load_to_db(db, news_dict: dict):
    # Check if news is existed. If not -> insert record
    if db['news'].find_one(news_dict) is None:
        db['news'].insert_one(news_dict)
        print(f"Inserted record {news_dict['link']}")


# Getting info from news page
def parse_news_data(links: list):
    dbname = get_database()
    for i in range(len(links)):
        resp = req.get(f"https://v102.ru{links[i]}")
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

        news_dict = {'link': links[i], 'article': article.text, 'date': date.text, 'text': news_text, 'comments': comments.text}
        load_to_db(dbname, news_dict)


def main():
    user_wait_time = input("Enter wait time in seconds: ")
    while True:
        try:
            user_wait_time = float(user_wait_time)
            if user_wait_time <= 0:
                raise "Wrong input. Your wait time cant be lower that 0!"
            break
        except Exception as e:
            print(f"{e}\nTry again")
        user_wait_time = input("Enter wait time in seconds: ")

    links = Queue()
    event_crawler = Event()
    th_crawler = Thread(target=crawler, args=(user_wait_time, event_crawler, links,))

    while True:
        th_crawler.start()
        th_crawler.join()


if __name__ == '__main__':
    main()
