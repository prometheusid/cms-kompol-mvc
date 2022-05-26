from project import app
import pickle
from flask import render_template, redirect, url_for, request, session

from project.models.Crawling import Crawling
from project.models.Sentiment import Sentiment
import twint

from project.models.Sentiment import Sentiment

@app.route("/dashboard/crawling/partai")
def cp_crawling_partai():
    title = ("Data Twitter")
    partai = Crawling.getKomunikatorPartai()
    tweet = Crawling.getTweetKomunikatorPartai()
    sentiment = Sentiment.predictPartai(tweet)
    data = Sentiment.mergedPartaiKomunikator(partai, sentiment)
    return render_template('panel/cp_crawling_partai/index.html', data=data, title=title)

@app.route("/dashboard/crawling/dprd")
def cp_crawling_dprd():
    title = ("Data Twitter")
    return render_template('panel/cp_crawling_dprd/index.html',title=title)

@app.route("/dashboard/crawling/partai/integritas")
def cp_crawling_partai_integritas():
    partais = Crawling.fetchPartai()
    for items in partais:
        c = twint.Config()
        c.Search = items['nama_partai']
        c.Pandas = True
        # diatur berdasarkan jumlah kebutuhan data
        c.Limit = 100
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        save = Crawling.integritasPartai(Tweets_df['tweet'], items['partai_id'])

    # return sesuai data yang dibutuhkan apa
    return "data berhasil disimpan"

@app.route("/dashboard/crawling/partai/komunikator")
def cp_crawling_partai_komunikator():
    partais = Crawling.fetchPartai()
    for items in partais:
        c = twint.Config()
        c.Search = items['account_head_leader']
        c.Pandas = True
        # diatur berdasarkan jumlah kebutuhan data
        c.Limit = 100
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        save = Crawling.komunikatorPartai(Tweets_df['tweet'], items['partai_id'])
    # return sesuai data yang dibutuhkan apa
    return "data berhasil disimpan"

@app.route("/dashboard/crawling/dprd/integritas")
def cp_crawling_dprd_integritas():
    dprds = Crawling.fetchDprd()
    for items in dprds:
        c = twint.Config()
        c.Search = items['akun_twitter']
        c.Pandas = True
        # diatur berdasarkan jumlah kebutuhan data
        c.Limit = 100
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        save = Crawling.integritasDprd(Tweets_df['tweet'], items['user_id'])
    # return sesuai data yang dibutuhkan apa
    return "data berhasil disimpan"


@app.route("/dashboard/predict")
def cp_predict():
    text = ['kata iwan fals anggota dewan jangan tidur kalau sidang soal rakyat']
    with open(f'{app.root_path}/static/model-nb/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(f'{app.root_path}/static/model-nb/tf_new.pkl', 'rb') as f:
        tf_new = pickle.load(f)
    
    textTf = tf_new.transform(text)
    prediction = model.predict(textTf)

    return str(prediction)