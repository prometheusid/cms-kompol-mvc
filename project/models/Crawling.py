import re

from sqlalchemy import true
from project import app
from project.config.Database import mysql
from datetime import datetime
from flask_mysqldb import MySQLdb
from functools import partial
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Crawling():
    def fetchPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_partai")
        data = cur.fetchall()
        return data
    
    def fetchDprd():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users WHERE role_id = 3")
        data = cur.fetchall()
        return data

    def integritasPartai(tweet, partaiId):
        cleanTweet = Crawling.cleanTweet(tweet)
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        for items in cleanTweet:
            cur.execute("INSERT INTO `tbl_crawling_integritas_partai` (`partai_id`, `tweet`, `created_at`, `updated_at`) VALUES (%s,%s,%s,%s)",
                    (partaiId, items, createdAt, createdAt))
        mysql.connection.commit()
        return len(cleanTweet)

    def komunikatorPartai(tweet, partaiId):
        cleanTweet = Crawling.cleanTweet(tweet)
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        for items in cleanTweet:
            cur.execute("INSERT INTO `tbl_crawling_komunikator_partai` (`partai_id`, `tweet`, `created_at`, `updated_at`) VALUES (%s,%s,%s,%s)",
                    (partaiId, items, createdAt, createdAt))
        mysql.connection.commit()
        return len(cleanTweet)

    def integritasDprd(tweet, userId):
        cleanTweet = Crawling.cleanTweet(tweet)
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        for items in cleanTweet:
            cur.execute("INSERT INTO `tbl_crawling_integritas_dprd` (`user_id`, `tweet`, `created_at`, `updated_at`) VALUES (%s,%s,%s,%s)",
                    (userId, items, createdAt, createdAt))
        mysql.connection.commit()
        return len(cleanTweet)
    
    def cleanTweet(tweet):
        # definisi slang Text
        with open(f'{app.root_path}/static/model-nb/slang.txt') as file:
            slang_map = dict(map(str.strip, line.partition('\t')[::2])
            for line in file if line.strip())

        slang_words = sorted(slang_map, key=len, reverse=True) # longest first for regex
        regex = re.compile(r"\b({})\b".format("|".join(map(re.escape, slang_words))))
        replaceSlang = partial(regex.sub, lambda m: slang_map[m.group(1)])

        # fungsi untuk clean dataset
        tweet = tweet.apply(lambda x: Crawling.casefoldingRemoveRt(x))
        tweet = tweet.apply(lambda x: Crawling.removeNoise(x))
        tweet = tweet.apply(lambda x: replaceSlang(x))
        tweet = tweet.apply(lambda x: Crawling.removePunctuation(x))

        # stopword
        tweet = tweet.apply(lambda x: Crawling.stopWord(x)) 

        # stemming
        tweet = tweet.apply(lambda x: Crawling.stemming(x))

        # delete missing value 
        nan_value = float('NaN')
        tweet.replace('', nan_value, inplace=True)
        tweet.dropna(inplace=True)

        # delete data duplicate
        tweet.drop_duplicates(keep = 'first', inplace = True)

        return tweet
    
    def casefoldingRemoveRt(text):
        # menghapus RT (reetwet)
        text = re.sub(r'^[RT]+', '', text) 
        # case folding (menjadi lower case)
        text = text.lower()
        # menghapus CC (carbon copy)
        text = re.sub(r'^[cc]+', '', text)
        return text

    # fungsi untuk menghapus noise
    def removeNoise(text): 
        # menghapus unicode
        text = re.sub(r'(\\u[0-9A-Fa-f]+)','', text)
        # menghapus emoticon
        text = re.sub(r'[^\x00-\x7f]','',text)
        # menghapus url
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text) 
        # menghapus # (biasanya utk menandai topik tertentu)
        text = re.sub(r'#([^\s]+)', '', text) 
        # menghapus "@users"
        text = re.sub('@[^\s]+','',text)
        return text

    def removePunctuation(text): 
        # menghapus integers/numbers
        text = ''.join([i for i in text if not i.isdigit()]) 
        # khusus untuk tanda baca ' (dirapatkan dengan text)
        text = re.sub("'",'',text)
        # menghapus punctuation (tanda baca)
        text = re.sub(r"[^A-Za-z]+"," ",text)
        # menghapus 1 karakter
        text = re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', text)
        # menghapus whitespace
        text = ' '.join(text.split())
        return text
    
    def stopWord(text):
        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()
        stop = stopword.remove(text)
        return stop

    def stemming(text):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stream = stemmer.stem(text)
        return stream


    