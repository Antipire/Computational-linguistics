from bs4 import BeautifulSoup
import requests as req
import time
from queue import Queue
from threading import Thread, Event, current_thread


def crawler(wait_time: int, event_crawler: Event, event_listener: Event, links: Queue):
    while True:
        resp = req.get(f"https://v102.ru/center_line_dorabotka_ajax.php?page=0&category=0")
        soup = BeautifulSoup(resp.text, 'lxml')
        page_links = []
        for a in soup.find_all("a", class_="detail-link-text", href=True):
            page_links.append(a['href'])
        links.put(page_links)
        event_listener.set()
        print(links.get())
        event_crawler.wait(wait_time)


# TODO: add code
# Pushing data to DB
def load_to_db():
    pass


# TODO: add code
# Getting info from news page
def parse_news_data():
    pass


# Checking if length of links array was changed
def array_listener(links: Queue, difference: list, event: Event):
    while True:
        if event.is_set():
            print("\nCan read Queue")
            event.clear()
        event.wait()


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

    links = Queue()
    difference = [0]
    event_crawler = Event()
    event_listener = Event()
    th_crawler = Thread(target=crawler, args=(user_wait_time, event_crawler, event_listener, links,))
    th_arr_listener = Thread(target=array_listener, args=(links, difference, event_listener,))

    while True:
        th_crawler.start()
        th_arr_listener.start()

        th_crawler.join()
        th_arr_listener.join()


if __name__ == '__main__':
    main()
