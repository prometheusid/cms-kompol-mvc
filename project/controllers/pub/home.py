
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
# Import Model
from project.models.LaporanKunjungan import LaporanKunjungan
from project.models.Info import Info
#route index
@app.route('/', methods = ['GET'])
def pub_home():
    title = ("KOMUNIKASI POLITIK")
    laporan = LaporanKunjungan.fetchKunjungan3()
    info = Info.fetchInfo3()
    return render_template('public/homepage/index.html', title=title, laporan=laporan, info=info)
