from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from os.path import join, dirname, realpath
from flask_mysqldb import MySQLdb
from werkzeug.utils import secure_filename
import os

class LaporanKunjungan:

    UPLOAD_FOLDER = join(dirname(realpath(__file__)), '../uploadedFiles')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    

    def fetchKunjungan3():
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM tbl_lapkun as a LEFT JOIN users as b ON a.user_id = b.user_id ORDER BY a.created_at DESC LIMIT 3")
        data = cur.fetchall()
        return data
    
    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in LaporanKunjungan.ALLOWED_EXTENSIONS

    def addDataLaporanKunjungan():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and LaporanKunjungan.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        author = session['id']
        judul = request.form['judul-laporan']
        isi = request.form['isi-laporan']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_lapkun (user_id, lapkun_judul, lapkun_isi, document, created_at) VALUES (%s,%s,%s,%s,%s)",
                    (author, judul, isi, filename, waktu))
        
        if session['role'] == 2:
            curl_users = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_users.execute("SELECT * FROM users WHERE user_id = %s", (author,))
            data_users= curl_users.fetchone()
            curl_users.close()

            id_partai = data_users['partai_id']

            curl_ahp_partai = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_ahp_partai.execute("SELECT * FROM tbl_ahp_partai WHERE partai_id = %s", (id_partai,))
            ahp_partai = curl_ahp_partai.fetchone()
            curl_ahp_partai.close()

            ahp_eksistensi_before = ahp_partai['laporan_jumlah']
            ahp_eksistensi = int(ahp_eksistensi_before) + 10

            update = mysql.connection.cursor()
            sql_update = "UPDATE tbl_ahp_partai SET laporan_jumlah = %s WHERE partai_id = %s"
            value_ahp = (ahp_eksistensi, id_partai)
            update.execute(sql_update, value_ahp)
        
        if session['role'] == 3:
            user_id = session['id']

            curl_ahp_dprd = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_ahp_dprd.execute("SELECT * FROM tbl_ahp_dprd WHERE user_id = %s", (user_id,))
            ahp_dprd = curl_ahp_dprd.fetchone()
            curl_ahp_dprd.close()

            ahp_laporan_jumlah_before = ahp_dprd['laporan_jumlah']
            ahp_laporan_jumlah = int(ahp_laporan_jumlah_before) + 10

            ahp_laporan_sentiment_before = ahp_dprd['laporan_sentiment']
            ahp_laporan_sentiment = int(ahp_laporan_sentiment_before) + 15

            update = mysql.connection.cursor()
            sql_update = "UPDATE tbl_ahp_dprd SET laporan_jumlah = %s, laporan_sentiment = %s WHERE user_id = %s"
            value_ahp = (ahp_laporan_jumlah, ahp_laporan_sentiment, user_id)
            update.execute(sql_update, value_ahp)
        
        mysql.connection.commit()

    def fetchLapkun():
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM tbl_lapkun as a LEFT JOIN users as b ON a.user_id = b.user_id ORDER BY a.created_at DESC")
        data = cur.fetchall()
        return data

    def detailLapkun(id):
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM tbl_lapkun as a \
            LEFT JOIN users as b ON a.user_id = b.user_id \
            WHERE a.lapkun_id=%s", (id,))
        data = cur.fetchone()
        return data
    
    def deleteDataLapkun(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tbl_lapkun WHERE lapkun_id=%s", (id,))
        mysql.connection.commit()