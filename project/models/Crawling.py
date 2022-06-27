import re

from project import app
from project.config.Database import mysql
from datetime import datetime
from functools import partial
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Crawling():
    def getAllRiwayatIntegritasDprd():
        cur = mysql.connection.cursor() 
        cur.execute("SELECT A.id, A.created_at, COUNT(B.integritas_dprd_riwayat_id) as jumlah from tbl_crawling_integritas_dprd_riwayat as A JOIN tbl_crawling_integritas_dprd as B ON A.id = B.integritas_dprd_riwayat_id GROUP BY B.integritas_dprd_riwayat_id")
        data = cur.fetchall()
        return data

    def getAllDataIntegritasDewan():
        cur = mysql.connection.cursor() 
        cur.execute("SELECT A.id, A.tweet, B.nama_user from tbl_crawling_integritas_dprd as A JOIN users as B ON A.user_id = B.user_id ORDER BY A.created_at DESC")
        data = cur.fetchall()
        return data

    def getAllRiwayatIntegritasPartai():
        cur = mysql.connection.cursor() 
        cur.execute("SELECT A.id, A.created_at, COUNT(B.integritas_partai_riwayat_id) as jumlah from tbl_crawling_integritas_partai_riwayat as A JOIN tbl_crawling_integritas_partai as B ON A.id = B.integritas_partai_riwayat_id GROUP BY B.integritas_partai_riwayat_id")
        data = cur.fetchall()
        return data
    
    def getAllRiwayatKomunikatorPartai():
        cur = mysql.connection.cursor() 
        cur.execute("SELECT A.id, A.created_at, COUNT(B.komunikator_partai_riwayat_id) as jumlah from tbl_crawling_komunikator_partai_riwayat as A JOIN tbl_crawling_komunikator_partai as B ON A.id = B.komunikator_partai_riwayat_id GROUP BY B.komunikator_partai_riwayat_id")
        data = cur.fetchall()
        return data

    def getAllDataIntegritasPartai():
        cur = mysql.connection.cursor() 
        cur.execute("SELECT A.id, A.tweet, B.nama_partai from tbl_crawling_integritas_partai as A JOIN tbl_partai as B ON A.partai_id = B.partai_id ORDER BY A.created_at DESC")
        data = cur.fetchall()
        return data
    
    def getAllDataKomunikatorPartai():
        cur = mysql.connection.cursor() 
        cur.execute("SELECT A.id, A.tweet, B.head_leader from tbl_crawling_komunikator_partai as A JOIN tbl_partai as B ON A.partai_id = B.partai_id ORDER BY A.created_at DESC")
        data = cur.fetchall()
        return data

    def createIntegritasDprdRiwayat():
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `tbl_crawling_integritas_dprd_riwayat` (`created_at`, `updated_at`) VALUES (%s,%s)",
                    (createdAt, createdAt))
        mysql.connection.commit()
        return cur.lastrowid

    def createKomunikatorPartaiRiwayat():
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `tbl_crawling_komunikator_partai_riwayat` (`created_at`, `updated_at`) VALUES (%s,%s)",
                    (createdAt, createdAt))
        mysql.connection.commit()
        return cur.lastrowid

    def createIntegritasPartaiRiwayat():
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `tbl_crawling_integritas_partai_riwayat` (`created_at`, `updated_at`) VALUES (%s,%s)",
                    (createdAt, createdAt))
        mysql.connection.commit()
        return cur.lastrowid

    def getIntegritasDprd():
        cur = mysql.connection.cursor() 
        cur.execute("SELECT a.user_id, a.nama_user, a.akun_twitter, c.nama_partai, COUNT('b.user_id') as jumlah_tweet from users as a JOIN tbl_crawling_integritas_dprd as b ON a.user_id = b.user_id JOIN tbl_partai as c ON a.partai_id = c.partai_id GROUP BY b.user_id ORDER BY a.user_id ASC")
        data = cur.fetchall()
        return data

    def getTweetIntegritasDprd():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_crawling_integritas_dprd ORDER BY user_id ASC")
        data = cur.fetchall()
        return data

    def getIntegritasPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT a.partai_id, a.nama_partai, a.head_leader, a.account_twitter, COUNT('b.partai_id') as jumlah_tweet from tbl_partai as a JOIN tbl_crawling_integritas_partai as b ON a.partai_id = b.partai_id GROUP BY b.partai_id ORDER BY a.partai_id ASC")
        data = cur.fetchall()
        return data
    
    def getTweetIntegritasPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_crawling_integritas_partai ORDER BY partai_id ASC")
        data = cur.fetchall()
        return data

    def getKomunikatorPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT a.partai_id, a.nama_partai, a.head_leader, a.account_head_leader, COUNT('b.partai_id') as jumlah_tweet from tbl_partai as a JOIN tbl_crawling_komunikator_partai as b ON a.partai_id = b.partai_id GROUP BY b.partai_id ORDER BY a.partai_id ASC")
        data = cur.fetchall()
        return data
    
    def getTweetKomunikatorPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_crawling_komunikator_partai ORDER BY partai_id ASC")
        data = cur.fetchall()
        return data

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

    def integritasPartai(tweet, partaiId, riwayatId):
        cleanTweet = Crawling.cleanTweet(tweet)
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        for items in cleanTweet:
            cur.execute("INSERT INTO `tbl_crawling_integritas_partai` (`partai_id`, `tweet`, `created_at`, `updated_at`, `integritas_partai_riwayat_id`) VALUES (%s,%s,%s,%s,%s)",
                    (partaiId, items, createdAt, createdAt, riwayatId))
        mysql.connection.commit()
        return len(cleanTweet)

    def komunikatorPartai(tweet, partaiId, riwayatId):
        cleanTweet = Crawling.cleanTweet(tweet)
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        for items in cleanTweet:
            cur.execute("INSERT INTO `tbl_crawling_komunikator_partai` (`partai_id`, `tweet`, `created_at`, `updated_at`, `komunikator_partai_riwayat_id`) VALUES (%s,%s,%s,%s,%s)",
                    (partaiId, items, createdAt, createdAt, riwayatId))
        mysql.connection.commit()
        return len(cleanTweet)

    def integritasDprd(tweet, userId, riwayatId):
        cleanTweet = Crawling.cleanTweet(tweet)
        createdAt = datetime.now()
        cur = mysql.connection.cursor()
        for items in cleanTweet:
            cur.execute("INSERT INTO `tbl_crawling_integritas_dprd` (`user_id`, `tweet`, `created_at`, `updated_at`, `integritas_dprd_riwayat_id`) VALUES (%s,%s,%s,%s,%s)",
                    (userId, items, createdAt, createdAt, riwayatId))
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