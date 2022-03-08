from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os

class Info:
    
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), '../uploadedFiles')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    def fetchInfo():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM info as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC")
        data = cur.fetchall()
        return data
    
    def fetchInfo3():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM info as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC LIMIT 6")
        data = cur.fetchall()
        return data

    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Info.ALLOWED_EXTENSIONS

    def addDataInfo():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and Info.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        author = session['id']
        judul = request.form['judul-info']
        isi = request.form['isi-info']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO info (user_id, judul_info, isi_info, thumb, created_at) VALUES (%s,%s,%s,%s, %s)",
                    (author, judul, isi, filename, waktu))
        mysql.connection.commit()

    def detailDataInfo(id):
        cur = mysql.connection.cursor()
        cur.execute(
        "SELECT * from info as a LEFT JOIN users as b ON a.user_id = b.user_id WHERE a.info_id=%s", (id,))
        data = cur.fetchone()
        return data

    def deleteDataInfo(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM info WHERE info_id=%s", (id,))
        mysql.connection.commit()