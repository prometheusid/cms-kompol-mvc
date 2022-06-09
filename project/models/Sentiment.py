import re

import pickle
import collections
from project import app
from itertools import count, groupby

class Sentiment():
    def predictDprd(data):
        tweets = []
        userIds = [] 
        merged = []
        total = []

        with open(f'{app.root_path}/static/model-nb/model80.pkl', 'rb') as f:
            model = pickle.load(f)
        with open(f'{app.root_path}/static/model-nb/tfidf80.pkl', 'rb') as f:
            tf_new = pickle.load(f)

        # memasukan data ke dalam array
        for item in data:
            tweets.append(item['tweet'])
            userIds.append(item['user_id'])

        textTf = tf_new.transform(tweets)
        # jika 1 dan 0 positive negative
        prediction = model.predict(textTf)

        for i in range(len(data)):
            merged.append((userIds[i],prediction[i]))

        counter=collections.Counter(userIds)
        userId = counter.keys()
        
        for i in userId:
            total.append({'user_id' : i, 'total_positive': merged.count((i, 1)) ,'total_negative': merged.count((i, 0))})
        return total

    def predictPartai(data):
        tweets = []
        partaiIds = [] 
        merged = []
        total = []

        with open(f'{app.root_path}/static/model-nb/model80.pkl', 'rb') as f:
            model = pickle.load(f)
        with open(f'{app.root_path}/static/model-nb/tfidf80.pkl', 'rb') as f:
            tf_new = pickle.load(f)

        # memasukan data ke dalam array
        for item in data:
            tweets.append(item['tweet'])
            partaiIds.append(item['partai_id'])

        textTf = tf_new.transform(tweets)
        # jika 1 dan 0 positive negative
        prediction = model.predict(textTf)

        for i in range(len(data)):
            merged.append((partaiIds[i],prediction[i]))

        counter=collections.Counter(partaiIds)
        partaiId = counter.keys()
        
        for i in partaiId:
            total.append({'partai_id' : i, 'total_positive': merged.count((i, 1)) ,'total_negative': merged.count((i, 0))})
        return total

    def mergedDprdIntegritas(dprds, sentiments):
        data = [];
        for dprd in dprds:
            for sentiment in sentiments:
                if dprd['user_id'] == sentiment['user_id']:
                    data.append({'user_id' : dprd['user_id'], 'nama' : dprd['nama_user'], 'partai' : dprd['nama_partai'],'akun_twitter' : dprd['akun_twitter'], 'jumlah_tweet' : dprd['jumlah_tweet'], 'total_positive' : sentiment['total_positive'], 'total_negative' : sentiment['total_negative']});
        return data

    def mergedPartaiKomunikator(partais, sentiments):
        data = [];
        for partai in partais:
            for sentiment in sentiments:
                if partai['partai_id'] == sentiment['partai_id']:
                    data.append({'partai_id' : partai['partai_id'], 'nama_partai' : partai['nama_partai'], 'head_leader' : partai['head_leader'], 'account_head_leader' : partai['account_head_leader'], 'jumlah_tweet' : partai['jumlah_tweet'], 'total_positive' : sentiment['total_positive'], 'total_negative' : sentiment['total_negative']});
        return data
    
    def mergedPartaiIntegritas(partais, sentiments):
        data = [];
        for partai in partais:
            for sentiment in sentiments:
                if partai['partai_id'] == sentiment['partai_id']:
                    data.append({'partai_id' : partai['partai_id'], 'nama_partai' : partai['nama_partai'], 'head_leader' : partai['head_leader'], 'account_twitter' : partai['account_twitter'], 'jumlah_tweet' : partai['jumlah_tweet'], 'total_positive' : sentiment['total_positive'], 'total_negative' : sentiment['total_negative']});
        return data
    
    def predictLapkun(data):
        CLEANR = re.compile('<.*?>')

        tweets = []
        partaiIds = [] 
        merged = []
        total = []

        with open(f'{app.root_path}/static/model-nb/model80.pkl', 'rb') as f:
            model = pickle.load(f)
        with open(f'{app.root_path}/static/model-nb/tfidf80.pkl', 'rb') as f:
            tf_new = pickle.load(f)

        # memasukan data ke dalam array
        for item in data:
            tweets.append(re.sub(CLEANR, '', item['tweet']))
            partaiIds.append(item['partai_id'])

        textTf = tf_new.transform(tweets)
        # jika 1 dan 0 positive negative
        prediction = model.predict(textTf)

        for i in range(len(data)):
            merged.append((partaiIds[i],prediction[i]))

        counter=collections.Counter(partaiIds)
        partaiId = counter.keys()
        
        for i in partaiId:
            total.append({'partai_id' : i, 'total_positive': merged.count((i, 1)) ,'total_negative': merged.count((i, 0))})
        return total