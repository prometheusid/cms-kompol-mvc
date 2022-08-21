from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
import bcrypt

from project.models.Dashboard import Dashboard
from project.models.DashboardPartai import DashboardPartai
from project.models.DashboardDewan import DashboardDewan
from project.models.Survey import Survey
from project.models.GenerateAhpPartai import GenerateAhpPartai
from project.models.GenerateAhpDewan import GenerateAhpDewan
from project.models.Crawling import Crawling
from project.models.Sentiment import Sentiment
from project.models.LaporanKunjungan import LaporanKunjungan

@app.route("/dashboard-dewan/<id>")
def dashboard_dewan(id):
    user = Dashboard.getUsers(id)

    countTweet = DashboardDewan.countTweet(session['id'])
    countSurvey = DashboardDewan.countSurvey(session['id'])
    countKunjungan = DashboardDewan.countKunjungan(session['id'])
    countAhpDewan = DashboardDewan.countAhpDewan(session['id'])
    return render_template('panel/cp_dashboard_dewan/index.html', user=user, countTweet=countTweet, countSurvey=countSurvey, countKunjungan=countKunjungan, countAhpDewan=countAhpDewan[0])

# Laporan Kunjungan
@app.route("/dashboard-dewan/lapkun")
def dashboard_dewan_lapkun():
    title = ("Laporan Kunjungan")

    data = DashboardDewan.fetchLapkun(session['id'])
    lapkunDewan = DashboardDewan.lapkunDewan(session['id'])
    return render_template('panel/cp_dashboard_dewan/lapkun.html', data=data, title=title, lapkunDetail=lapkunDewan[0])

@app.route("/dashboard-dewan/lapkun/refresh" , methods=["POST"])
def dashboard_partai_dewan_refresh():
    GenerateAhpPartai.updateSurvey()
    GenerateAhpPartai.updateJumlahLapkun()
    GenerateAhpPartai.updateSentimentLapkun()
    GenerateAhpPartai.updateIntegritas()
    GenerateAhpPartai.updateKomunikator()

    GenerateAhpDewan.updateIntegritas()
    GenerateAhpDewan.updateJumlahLapkun()
    GenerateAhpDewan.updateSentimentLapkun()
    GenerateAhpDewan.updateForum()
    GenerateAhpDewan.updateKompetensiAkademik()
    GenerateAhpDewan.updateKompetensiExperience()
    GenerateAhpDewan.updateSurvey()

    return redirect(url_for('dashboard_dewan_lapkun'))

@app.route("/dashboard-dewan/lapkun/delete/<int:id>")
def hapus_lapkun_dewan(id):
    data = LaporanKunjungan.deleteDataLapkun(id)
    return redirect(url_for('dashboard_dewan_lapkun'))

# Survey
@app.route("/dashboard-dewan/survey")
def dashboard_dewan_survey():
    title = ("Hasil Survey")

    dewan = DashboardDewan.countSurveyDewan(session['id'])
    return render_template('panel/cp_dashboard_dewan/survey.html', title=title, dewan=dewan[0])

@app.route("/dashboard-dewan/survey/refresh" , methods=["POST"])
def dashboard_dewan_survey_refresh():
    # generate AHP Partai
    GenerateAhpPartai.updateSurvey()
    GenerateAhpPartai.updateJumlahLapkun()
    GenerateAhpPartai.updateSentimentLapkun()
    GenerateAhpPartai.updateIntegritas()
    GenerateAhpPartai.updateKomunikator()

    GenerateAhpDewan.updateIntegritas()
    GenerateAhpDewan.updateJumlahLapkun()
    GenerateAhpDewan.updateSentimentLapkun()
    GenerateAhpDewan.updateForum()
    GenerateAhpDewan.updateKompetensiAkademik()
    GenerateAhpDewan.updateKompetensiExperience()
    GenerateAhpDewan.updateSurvey()

    return redirect(url_for('dashboard_dewan_survey'))

# AHP
@app.route("/dashboard-dewan/ahp")
def dashboard_dewan_ahp():
    title = ("Hasil Ahp")
    user = Dashboard.getUsers(session['id'])

    partai = DashboardPartai.countAhpPartai(user['partai_id'])
    jumlah = DashboardPartai.countPartai()
    # dewan = DashboardPartai.countAhpDewan(user['partai_id'])
    # return str(partai)
    return render_template('panel/cp_dashboard_dewan/ahp.html', title=title, partai=partai[0], jumlah=jumlah)

@app.route("/dashboard-dewan/ahp/refresh" , methods=["POST"])
def dashboard_dewan_ahp_refresh():
    GenerateAhpPartai.updateSurvey()
    GenerateAhpPartai.updateJumlahLapkun()
    GenerateAhpPartai.updateSentimentLapkun()
    GenerateAhpPartai.updateIntegritas()
    GenerateAhpPartai.updateKomunikator()

    GenerateAhpDewan.updateIntegritas()
    GenerateAhpDewan.updateJumlahLapkun()
    GenerateAhpDewan.updateSentimentLapkun()
    GenerateAhpDewan.updateForum()
    GenerateAhpDewan.updateKompetensiAkademik()
    GenerateAhpDewan.updateKompetensiExperience()
    GenerateAhpDewan.updateSurvey()

    return redirect(url_for('dashboard_dewan_ahp'))

# Data Twitter
@app.route("/dashboard-dewan/tweet")
def dashboard_dewan_tweet():
    title = ("Data Twitter")

    dprdIntegritas = DashboardDewan.getIntegritasDprd(session['id'])
    tweetIntegritas = DashboardDewan.getTweetIntegritasDprd(session['id'])
    sentimentIntegritas = Sentiment.predictDprd(tweetIntegritas)
    dataIntegritas = Sentiment.mergedDprdIntegritas(dprdIntegritas, sentimentIntegritas)

    data = DashboardDewan.getAllDataIntegritasDewanById(session['id'])
    return render_template('panel/cp_dashboard_dewan/tweet.html', data=data, title=title, integritas=dataIntegritas)

@app.route("/dashboard-dewan/tweet/refresh" , methods=["POST"])
def dashboard_dewan_tweet_refresh():
    GenerateAhpPartai.updateSurvey()
    GenerateAhpPartai.updateJumlahLapkun()
    GenerateAhpPartai.updateSentimentLapkun()
    GenerateAhpPartai.updateIntegritas()
    GenerateAhpPartai.updateKomunikator()

    GenerateAhpDewan.updateIntegritas()
    GenerateAhpDewan.updateJumlahLapkun()
    GenerateAhpDewan.updateSentimentLapkun()
    GenerateAhpDewan.updateForum()
    GenerateAhpDewan.updateKompetensiAkademik()
    GenerateAhpDewan.updateKompetensiExperience()
    GenerateAhpDewan.updateSurvey()

    return redirect(url_for('dashboard_dewan_tweet'))
