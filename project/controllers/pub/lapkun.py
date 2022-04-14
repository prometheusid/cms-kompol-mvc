from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

"""
    Import MOdels
from project.models.Hello import Hello
"""
from project.models.LaporanKunjungan import LaporanKunjungan
# route index


@app.route("/kunjungan/")
def lapkun():
    title = ('LAPORAN KUNJUNGAN')
    data = LaporanKunjungan.fetchLapkun()
    return render_template("/public/lapkun/index.html", data=data, title=title)


@app.route("/kunjungan/thread/<int:id>")
def lapkun_thread(id):
    title = ('LAPORAN KUNJUNGAN')
    data = LaporanKunjungan.detailLapkun(id)

    # Get Count commentar
    # count = mysql.connection.cursor()
    # count.execute(
    #     "SELECT count('lapkun_id') FROM tbl_detail_forum  WHERE lapkun_id=%s", (id,))
    # num_of_items = [v for v in count.fetchone().values()][0]

    # Get data commentar
    # com = mysql.connection.cursor()
    # com.execute(
    #     "SELECT * FROM tbl_detail_forum as a JOIN users as b ON a.user_id = b.user_id WHERE a.lapkun_id=%s", (id,))
    # comment = com.fetchall()
    return render_template("/public/lapkun/thread.html", data=data, title=title, id=id)


@app.route("/kunjungan/thread/<int:id>", methods=["POST"])
def komentarlapkun(id):
    idKomen = request.form['idKomen']
    idLapkun = request.form['idLapkun']
    komen = request.form['komen']
    komenUser = session['id']
    waktu = datetime.now()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbl_detail_forum (id_detail_forum, lapkun_id, komentar, user_id, created_at) VALUES (%s,%s,%s,%s,%s)",
                (idKomen, idLapkun, komen, komenUser, waktu))
    mysql.connection.commit()
    return redirect(url_for('lapkun_thread', id=id))


@app.route("/kunjungan/tambahlaporan", methods=["GET", "POST"])
def tambahlaporan():
    title = ("LAPORAN KUNJUNGAN")
    if request.method == 'GET':
        return render_template('public/lapkun/tambahlaporan.html', title=title)
    else:
        data = LaporanKunjungan.addDataLaporanKunjungan()
    return redirect(url_for('lapkun'))

# @app.route('/uploads/<filename>')
# def uploadedFiles(filename=''):
#     from flask import send_from_directory
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
