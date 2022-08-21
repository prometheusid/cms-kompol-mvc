from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
import bcrypt

from project.models.Dashboard import Dashboard
from project.models.DashboardPartai import DashboardPartai
from project.models.Survey import Survey
from project.models.GenerateAhpPartai import GenerateAhpPartai
from project.models.GenerateAhpDewan import GenerateAhpDewan
from project.models.Crawling import Crawling
from project.models.Sentiment import Sentiment

@app.route("/dashboard-partai/<id>")
def dashboard_partai(id):
    user = Dashboard.getUsers(id)
    countDprd = DashboardPartai.countDprd(user['partai_id'])
    countSurvey = DashboardPartai.countSurvey(user['partai_id'])
    countKunjungan = DashboardPartai.countKunjungan(user['partai_id'])
    countAhpPartai = DashboardPartai.countAhpPartai(user['partai_id'])

    return render_template('panel/cp_dashboard_partai/index.html', user=user, countDprd=countDprd, countKunjungan=countKunjungan, countAhpPartai=countAhpPartai[0], countSurvey=countSurvey)

@app.route("/dashboard-partai/anggota")
def cp_dashboard_partai_anggota():
    title = ("TAMBAH ANGGOTA")
    cur = mysql.connection.cursor()
    cur.execute("SELECT partai_id from users WHERE user_id=%s", (session['id'],))
    user = cur.fetchone()
   
    par = mysql.connection.cursor()
    par.execute("SELECT a.user_id, a.nama_user, a.email_user, b.nama_partai FROM users as A\
                JOIN tbl_partai as b ON a.partai_id = b.partai_id WHERE a.role_id = 3 AND a.partai_id =%s\
                ORDER BY a.created_at DESC", (user['partai_id'],))
    data = par.fetchall()
    return render_template('panel/cp_dashboard_partai/anggota.html', data=data, title=title)

@app.route("/dashboard-partai/anggota/delete/<int:id>")
def dashboard_partai_hapus_anggota(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE user_id=%s" % (id))
    mysql.connection.commit()

    # hapus juga yang ada di ahp dprd
    curl = mysql.connection.cursor()
    curl.execute("DELETE FROM tbl_ahp_dprd WHERE user_id=%s" % (id))
    mysql.connection.commit()
    
    return redirect(url_for('cp_dashboard_partai_anggota'))

@app.route("/dashboard-partai/anggota/create", methods=["POST"])
def dashboard_partai_create_anggota(): 
    nameAnggota = request.form['nameAnggota']
    emailAnggota = request.form['emailAnggota']
    passwordAnggota = request.form['passwordAnggota'].encode('utf-8')
    hash_password = bcrypt.hashpw(passwordAnggota, bcrypt.gensalt())
    created = datetime.now()

    par = mysql.connection.cursor()
    par.execute("SELECT partai_id from users WHERE user_id=%s", (session['id'],))
    user = par.fetchone()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (nama_user, email_user, password, role_id, partai_id, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                    (nameAnggota, emailAnggota, hash_password, 3, user['partai_id'], created))
    mysql.connection.commit()

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO tbl_ahp_dprd (user_id, kompetensi_akademik,\
                    kompetensi_experience, popularitas_eksistensi, popularitas_citra,\
                    forum_jumlah, forum_sentiment, laporan_jumlah, laporan_sentiment,\
                    integritas_jumlah, integritas_sentiment, created_at, updated_at)\
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (cur.lastrowid, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, created, created))
    mysql.connection.commit()

    return redirect(url_for('cp_dashboard_partai_anggota'))

# Laporan Kunjungan
@app.route("/dashboard-partai/lapkun")
def dashboard_partai_lapkun():
    title = ("Laporan Kunjungan")
    user = Dashboard.getUsers(session['id'])
    lapkun = DashboardPartai.lapkun(user['partai_id'])
    sentimentLapkun = DashboardPartai.sentimentLapkun(user['partai_id'])
    lapkunDewan = DashboardPartai.lapkunDewan(user['partai_id'])
    return render_template('panel/cp_dashboard_partai/lapkun.html', title=title, lapkunDewan=lapkunDewan, lapkun=lapkun, sentimentLapkun=sentimentLapkun)

@app.route("/dashboard-partai/lapkun/refresh" , methods=["POST"])
def dashboard_partai_lapkun_refresh():
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

    return redirect(url_for('dashboard_partai_lapkun'))

# Survey
@app.route("/dashboard-partai/survey")
def dashboard_partai_survey():
    title = ("Hasil Survey")
    user = Dashboard.getUsers(session['id'])

    partai = DashboardPartai.countSurveyPartai(user['partai_id'])
    dewan = DashboardPartai.countSurveyDewan(user['partai_id'])
    return render_template('panel/cp_dashboard_partai/survey.html', title=title, partai=partai, dewan=dewan)

@app.route("/dashboard-partai/survey/refresh" , methods=["POST"])
def dashboard_partai_survey_refresh():
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

    return redirect(url_for('dashboard_partai_survey'))

# AHP
@app.route("/dashboard-partai/ahp")
def dashboard_partai_ahp():
    title = ("Hasil Ahp")
    user = Dashboard.getUsers(session['id'])

    partai = DashboardPartai.countAhpPartai(user['partai_id'])
    dewan = DashboardPartai.countAhpDewan(user['partai_id'])
    jumlah = DashboardPartai.countPartai()
    return render_template('panel/cp_dashboard_partai/ahp.html', title=title, partai=partai[0], jumlah=jumlah, dewan=dewan)

@app.route("/dashboard-partai/ahp/refresh" , methods=["POST"])
def dashboard_partai_ahp_refresh():
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

    return redirect(url_for('dashboard_partai_ahp'))

# Data Twitter
@app.route("/dashboard-partai/tweet")
def dashboard_partai_tweet():
    title = ("Data Twitter")
    user = Dashboard.getUsers(session['id'])

    partaiKomunikator = DashboardPartai.getKomunikatorPartaiById(user['partai_id'])
    tweetKomunikator = Crawling.getTweetKomunikatorPartai()
    sentimentKomunikator = Sentiment.predictPartai(tweetKomunikator)
    dataKomunikator = Sentiment.mergedPartaiKomunikator(partaiKomunikator, sentimentKomunikator)

    partaiIntegritas = DashboardPartai.getIntegritasPartaiById(user['partai_id'])
    tweetIntegritas = Crawling.getTweetIntegritasPartai()
    sentimentIntegritas = Sentiment.predictPartai(tweetIntegritas)
    dataIntegritas = Sentiment.mergedPartaiIntegritas(partaiIntegritas, sentimentIntegritas)

    return render_template('panel/cp_dashboard_partai/tweet.html', title=title, kom=dataKomunikator, integritas=dataIntegritas)

@app.route("/dashboard-partai/tweet/refresh" , methods=["POST"])
def dashboard_partai_tweet_refresh():
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

    return redirect(url_for('dashboard_partai_tweet'))

@app.route("/dashboard-partai/tweet/integritas")
def dashboard_partai_tweet_integritas():
    title = ("Data Integritas Partai")
    user = Dashboard.getUsers(session['id'])

    data = DashboardPartai.getAllDataIntegritasPartaiById(user['partai_id'])
    return render_template('panel/cp_dashboard_partai/integritas.html', title=title, data=data)

@app.route("/dashboard-partai/tweet/komunikator")
def dashboard_partai_tweet_komunikator():
    title = ("Data Komunikator Partai")
    user = Dashboard.getUsers(session['id'])

    data = DashboardPartai.getAllDataKomunikatorPartaiById(user['partai_id'])
    return render_template('panel/cp_dashboard_partai/komunikator.html', title=title, data=data)

# c