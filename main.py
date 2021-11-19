from bs4 import BeautifulSoup
import requests as req
import time
from threading import Thread, Event, current_thread


def crawler(wait_time: int, event: Event, links: list):
    while True:
        resp = req.get(f"https://v102.ru/center_line_dorabotka_ajax.php?page=0&category=0")
        soup = BeautifulSoup(resp.text, 'lxml')
        for a in soup.find_all("a", class_="detail-link-text", href=True):
            links.append(a['href'])

        event.wait(wait_time)


# TODO: add code
# Pushing data to DB
def load_to_db():
    pass


# TODO: add code
# Getting info from news page
def parse_news_data():
    pass


# Checking if length of links array was changed
def array_listener(links: list, difference: list, event: Event):
    while True:
        stored_array_len = len(links)
        event.wait(5)
        if len(links) != stored_array_len:
            difference[0] = len(links) - stored_array_len


def main():
    user_wait_time = input("Enter wait time in seconds: ")
    while True:
        try:
            user_wait_time = int(user_wait_time)
            if user_wait_time <= 0:
                raise "Wrong input. Your wait time cant be lower that 0!"
            break
        except Exception as e:
            print(f"{e}\nTry again")
        user_wait_time = input("Enter wait time in seconds: ")\

    links = []
    difference = [0]
    event = Event()
    th_crawler = Thread(target=crawler, args=(user_wait_time, event, links,))
    th_arr_listener = Thread(target=array_listener, args=(links, difference, event,))

    while True:
        th_crawler.start()
        th_arr_listener.start()

        th_crawler.join()
        th_arr_listener.join()


if __name__ == '__main__':
    main()
