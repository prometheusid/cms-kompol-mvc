from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os

class LaporanKunjungan:

    UPLOAD_FOLDER = join(dirname(realpath(__file__)), '../uploadedFiles')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    

    def fetchKunjungan3():
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM tbl_lapkun as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC LIMIT 3")
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
        mysql.connection.commit()