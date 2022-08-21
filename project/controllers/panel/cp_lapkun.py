
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# generate random integer values
from random import seed
from random import randint

# Import models
from project.models.LaporanKunjungan import LaporanKunjungan

#route index
@app.route("/dashboard/cp_lapkun")
def cp_lapkun():
    title = ("Data Laporan Kunjungan")
    # fetch data from model
    data = LaporanKunjungan.fetchLapkun()
    lapkunPartai = LaporanKunjungan.countLapkunPartai()
    lapkunDewan = LaporanKunjungan.countLapkunDewan()
    return render_template('panel/cp_lapkun/index.html', data=data, title=title, partai=lapkunPartai, dewan=lapkunDewan)

@app.route("/dashboard/cp_lapkun/delete/<int:id>")
def hapus_lapkun(id):
    data = LaporanKunjungan.deleteDataLapkun(id)
    return redirect(url_for('cp_lapkun'))

# testing for lapkun
@app.route("/dashboard/cp_lapkun/detail")
def cp_lapkun_detail():
    title = ("Data Laporan Kunjungan")
    # fetch data from model
    data = LaporanKunjungan.countLapkunDewan()
    return str(data)