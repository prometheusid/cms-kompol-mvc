from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
import bcrypt

from project.models.Dashboard import Dashboard
from project.models.Survey import Survey

@app.route("/dashboard-dewan/<id>")
def dashboard_dewan(id):
    user = Dashboard.getUsers(id)
    countDprd = Dashboard.countDprd()
    countPartai = Dashboard.countPartai()
  
    countWarga = Dashboard.countWarga()
    countInfo = Dashboard.countInfo()
    countSurveyPartai = Survey.countSurveyPartai()
    countSurveyDprd = Survey.countSurveyDPRD()
    return render_template('panel/cp_dashboard_dewan/index.html', user=user, countSurveyPartai=countSurveyPartai, countSurveyDprd=countSurveyDprd, countDprd=countDprd, countInfo=countInfo, countPartai=countPartai, countWarga=countWarga)

@app.route("/dashboard-dewan/anggota")
def cp_dashboard_dewan_anggota():
    title = ("TAMBAH ANGGOTA")
    cur = mysql.connection.cursor()
    cur.execute("SELECT partai_id from users WHERE user_id=%s", (session['id'],))
    user = cur.fetchone()
   
    par = mysql.connection.cursor()
    par.execute("SELECT a.user_id, a.nama_user, a.email_user, b.nama_partai FROM users as A\
                JOIN tbl_partai as b ON a.partai_id = b.partai_id WHERE a.role_id = 3 AND a.partai_id =%s\
                ORDER BY a.created_at DESC", (user['partai_id'],))
    data = par.fetchall()
    return render_template('panel/cp_dashboard_dewan/anggota.html', data=data, title=title)

@app.route("/dashboard-dewan/anggota/delete/<int:id>")
def dashboard_dewan_hapus_anggota(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE user_id=%s" % (id))
    mysql.connection.commit()
    return redirect(url_for('cp_dashboard_dewan_anggota'))

@app.route("/dashboard-dewan/anggota/create", methods=["POST"])
def dashboard_dewan_create_anggota(): 
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

    return redirect(url_for('cp_dashboard_dewan_anggota'))