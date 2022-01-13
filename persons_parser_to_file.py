from bs4 import BeautifulSoup
import requests as req
import time

file = open('persons.txt', 'w+')
file.write('#encoding "utf-8"\n\nPersons -> ')
for i in range(10):

    resp = req.get(f"https://global-volgograd.ru/person?offset={i*20}")
    soup = BeautifulSoup(resp.text, 'lxml')

    persons_raw = soup.find_all("div", class_="person-text")

    for person in persons_raw:
        FIO = person.text.split()[:3]
        file.write(f"\"{FIO[0]}\"|\n")

    time.sleep(2)

file.close()
