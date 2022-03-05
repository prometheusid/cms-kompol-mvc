from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# Import models
from project.models.Ahp import Ahp
from project.models.Criteria import Criteria


# #route index

# 1. index untuk menampilkan data keseluruhan
# 2. create untuk tombol memlih create/or function dll.
# 3. store create/add from database(menyimpan)
# 4. show (menampilkan satu bagian)
# 5. edit (untuk redirect tombol edit)
# 6. update (untuk update data yg baru)
# 7. destroy (hapus)

@app.route("/dashboard/ahp/partai")
def cp_ahp_partai():
    title = ("Ahp Partai")
    # fetch data from model
    # TODO : tampilkan semua data dan bisa melakukan perhitungan lagi.
    # untuk Score mending lakukakn dengan ulang agar score bisa diambil dari data yg paling baru
    data = Ahp.fetchValue()
    return render_template('panel/cp_ahp_partai/index.html', data=data, title=title)

@app.route("/dashboard/ahp/bobot", methods=["GET", "POST"])
def cp_ahp_partai_bobot():
    title = ("Ahp bobot")
    # fetch data from model
    # TODO : tampilkan semua data dan bisa melakukan perhitungan lagi.
    # untuk Score mending lakukakn dengan ulang agar score bisa diambil dari data yg paling baru
    data = Ahp.fetchValue()
    criteria = ""
    if (request.form) :
        c12 = request.form['c12']
        c13 = request.form['c13']
        c14 = request.form['c14']
        c23 = request.form['c23']
        c24 = request.form['c24']
        c34 = request.form['c34']
        criteria = Criteria.perbandingan([c12, c13, c14, c23, c24, c34], 4)

    return render_template('panel/cp_ahp_partai/bobot.html', data=data, criteria=str(criteria), title=title)

@app.route("/dashboard/ahp/partai/test", methods=["GET", "POST"]) 
def cp_ahp_partai_q():
    title = ("Ahp Partai")
    # fetch data from model
    # TODO : tampilkan semua data dan bisa melakukan perhitungan lagi.
    # untuk Score mending lakukakn dengan ulang agar score bisa diambil dari data yg paling baru
    c12 = request.form['c12']
    c13 = request.form['c13']
    c14 = request.form['c14']
    c23 = request.form['c23']
    c24 = request.form['c24']
    c34 = request.form['c34']
    # data = Criteria.perbandingan([3, 3, 5, 3, 3, 3], 4)
    data = Criteria.perbandingan([c12, c13, c14, c23, c24, c34], 4)
    return str(data)

# @app.route("/survey/tambah-question", methods=["GET", "POST"])
# def cp_survey_question():
#     data = Survey.addDataQuestion()
#     return redirect(url_for('cp_survey'))