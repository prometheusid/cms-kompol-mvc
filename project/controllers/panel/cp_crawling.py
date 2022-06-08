import pickle
import twint

from project import app
from flask import render_template, redirect, url_for
from project.models.Crawling import Crawling
from project.models.Sentiment import Sentiment
from project.models.Sentiment import Sentiment

@app.route("/dashboard/crawling/partai")
def cp_crawling_partai():
    title = ("Data Twitter")

    partaiKomunikator = Crawling.getKomunikatorPartai()
    tweetKomunikator = Crawling.getTweetKomunikatorPartai()
    sentimentKomunikator = Sentiment.predictPartai(tweetKomunikator)
    dataKomunikator = Sentiment.mergedPartaiKomunikator(partaiKomunikator, sentimentKomunikator)

    partaiIntegritas = Crawling.getIntegritasPartai()
    tweetIntegritas = Crawling.getTweetIntegritasPartai()
    sentimentIntegritas = Sentiment.predictPartai(tweetIntegritas)
    dataIntegritas = Sentiment.mergedPartaiIntegritas(partaiIntegritas, sentimentIntegritas)

    return render_template('panel/cp_crawling_partai/index.html', integritas=dataIntegritas, komunikator=dataKomunikator, title=title)

@app.route("/dashboard/crawling/dprd")
def cp_crawling_dprd():
    title = ("Data Twitter")
    return render_template('panel/cp_crawling_dprd/index.html',title=title)

@app.route("/dashboard/crawling/partai/integritas", methods=["POST"])
def cp_crawling_partai_integritas():
    partais = Crawling.fetchPartai()
    for items in partais:
        c = twint.Config()
        c.Search = items['nama_partai']
        c.Pandas = True
        # diatur berdasarkan jumlah kebutuhan data
        c.Limit = 10
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        save = Crawling.integritasPartai(Tweets_df['tweet'], items['partai_id'])

    # return sesuai data yang dibutuhkan apa
    return redirect(url_for('cp_crawling_partai'))

@app.route("/dashboard/crawling/partai/komunikator", methods=["POST"])
def cp_crawling_partai_komunikator():
    partais = Crawling.fetchPartai()
    for items in partais:
        c = twint.Config()
        c.Search = items['account_head_leader']
        c.Pandas = True
        # diatur berdasarkan jumlah kebutuhan data
        c.Limit = 10
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        save = Crawling.komunikatorPartai(Tweets_df['tweet'], items['partai_id'])
    # return sesuai data yang dibutuhkan apa
    return redirect(url_for('cp_crawling_partai'))

@app.route("/dashboard/crawling/dprd/integritas", methods=["POST"])
def cp_crawling_dprd_integritas():
    dprds = Crawling.fetchDprd()
    for items in dprds:
        c = twint.Config()
        c.Search = items['akun_twitter']
        c.Pandas = True
        # diatur berdasarkan jumlah kebutuhan data
        c.Limit = 10
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        save = Crawling.integritasDprd(Tweets_df['tweet'], items['user_id'])
    # return sesuai data yang dibutuhkan apa
    return "data berhasil disimpan"