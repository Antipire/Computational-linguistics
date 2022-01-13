from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import IDF
from pyspark.ml.feature import Word2Vec
# from lxml import etree
import re
import string
import pymongo
import numpy as np


def remove_punctuation(text):
    """
    Удаление пунктуации из текста
    """
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_linebreaks(text):
    """
    Удаление разрыва строк из текста
    """
    return text.strip()


def get_only_words(tokens):
    """
    Получение списка токенов, содержащих только слова
    """
    return list(filter(lambda x: re.match('[a-zA-Z]+', x), tokens))


spark = SparkSession \
    .builder \
    .appName("SimpleApplication") \
    .getOrCreate()

client = pymongo.MongoClient("mongodb+srv://DB_NEWS_DATA:1234@cluster0.wshon.mongodb.net/news_data")
database = client["news_data"]
collection = database["news_collection"]
for news in collection.find({}):
    with open("input.txt", "a") as f:
        print(i)
        f.write(news['text'])


input_data = spark.sparkContext.wholeTextFiles('input.txt')

prepared_data = input_data.map(lambda x: (x[0], remove_punctuation(x[1])))

prepared_df = prepared_data.toDF().selectExpr('_2 as text')


# Разбить claims на токены
tokenizer = Tokenizer(inputCol="text", outputCol="words")
words_data = tokenizer.transform(prepared_df)


# Удалить стоп-слова (союзы, предлоги, местоимения и т.д.)
stop_words = StopWordsRemover.loadDefaultStopWords('russian')
stop_words.append(r"")
remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)
filtered = remover.transform(words_data)

vectorizer = CountVectorizer(inputCol='filtered', outputCol='raw_features').fit(filtered)

word2Vec = Word2Vec(vectorSize=35, minCount=0, inputCol='words', outputCol='result')
model = word2Vec.fit(words_data)
w2v_df = model.transform(filtered)
w2v_df.show()


vocabulary = vectorizer.vocabulary

with open("people.txt", "r") as f:
  data = f.read()
  data = data.replace("\"", "").replace("|", "")
  data = data.lower().split("\n")
f.close()
for vip in data:
    if vip in vocabulary:
        vips = model.findSynonyms(vip, 5).collect()
        syn_dict = {'Person': vip, '1:': vips[0][0], '2:': vips[1][0], '3:': vips[2][0], '4:': vips[3][0], '5:': vips[4][0]}
        database['synonyms'].insert_one(syn_dict)


with open("sights.txt", "r") as f:
  data = f.read()
  data = data.replace("\"", "").replace(" |", "")
  data = data.lower().split("\n")
f.close()
for vip in data:
    if vip in vocabulary:
        vips = model.findSynonyms(vip, 5).collect()
        syn_dict = {'Object': vip, '1:': vips[0][0], '2:': vips[1][0], '3:': vips[2][0], '4:': vips[3][0], '5:': vips[4][0]}
        database['synonyms'].insert_one(syn_dict)


spark.stop()