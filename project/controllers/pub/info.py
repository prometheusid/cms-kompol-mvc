from project import app
from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime
from project.config.Database import mysql
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "uploadedFiles"
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#index info
@app.route('/info', methods = ['GET'])
def info():
    title = ("INFO PUBLIK")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM info as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC")
    data = cur.fetchall()
    return render_template('public/info/index.html', data = data, title = title)

# Tambah Info
@app.route("/pub_info/tambahinfo", methods=["GET", "POST"])
def tambahinfo():
    title = ("INFO PUBLIK")
    if request.method == 'GET':
        return render_template('public/info/tambahinfo.html', title=title)
    else:
        author = session['id']
        judul = request.form['judul-info']
        isi = request.form['isi-info']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO info (user_id, judul_info, isi_info, created_at) VALUES (%s,%s,%s,%s)",
                    (author, judul, isi, waktu))
        mysql.connection.commit()
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('info', title=title))
    return redirect(url_for('info', title=title))

# Detail Info
@app.route('/info/detail/<int:id>')
def detailinfo(id):
    title = ("INFO PUBLIK")
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from info as a LEFT JOIN users as b ON a.user_id = b.user_id WHERE a.info_id=%s", (id,))
    data = cur.fetchone()
    return render_template('public/info/detail.html', data=data, title=title)