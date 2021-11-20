from bs4 import BeautifulSoup
import requests as req


# Test page is https://v102.ru/news/96019.html

resp = req.get(f"https://v102.ru/news/96019.html")
soup = BeautifulSoup(resp.text, 'lxml')

# Get article headline
article = soup.find("h1", {'itemprop': "headline"})
print(article.text)

# Get news publishing date
date = soup.find("span", class_="date-new")
print(date.text)

# Get news text
# Current issue: Cant print value of news_text
#                when replacing \n. Idk why...
news = soup.find_all("div", class_="n-text")
news_text = ""
for item in news:
    news_text += str(item.text)
#news_text = news_text.replace('\n', ' ').replace(u'\xa0', "")
print(news_text)
