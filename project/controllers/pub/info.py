from project import app
from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime
from project.config.Database import mysql

# Import models
from project.models.Info import Info


#index info
@app.route('/info', methods = ['GET'])
def info():
    title = ("INFO PUBLIK")
    data = Info.fetchInfo()
    return render_template('public/info/index.html', data = data, title = title)

# Tambah Info
@app.route("/pub_info/tambahinfo", methods=["GET", "POST"])
def tambahinfo():
    title = ("INFO PUBLIK")
    if request.method == 'GET':
        return render_template('public/info/tambahinfo.html', title=title)
    else:
        data = Info.addDataInfo()
    return redirect(url_for('info', title=title))

# Detail Info
@app.route('/info/detail/<int:id>')
def detailinfo(id):
    title = ("INFO PUBLIK")
    data = Info.detailDataInfo(id)
    return render_template('public/info/detail.html', data=data, title=title)

@app.route('/uploads/<filename>')
def uploadedFiles(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)