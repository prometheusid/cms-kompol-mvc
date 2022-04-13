from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# Import models
from project.models.Ahp import Ahp
from project.models.Calculate import Calculate
from project.models.Criteria import Criteria


@app.route("/dashboard/ahp/dewan")
def cp_ahp_dewan():
    # TODO : get konstatnta from table criteria ahp
    # 2. menmpilkan contoh perhitungan yang akan dipakai
    # 3. bisa menampilkan data yang digunakan
    return render_template('panel/cp_ahp_dewan/index.html')

@app.route("/dashboard/ahp/bobot/dewan", methods=["GET", "POST"])
def cp_ahp_bobot_dewan():
    title = ("Ahp bobot")
    ahp = Ahp.fetchCriteriaPartai()
    return str(ahp)
    # value = Criteria.perbandingan([ahp['c12'], ahp['c13'], ahp['c14'], ahp['c23'], ahp['c24'], ahp['c34']], 4)
    # criteria = ""
    # if (request.form) :
    #     c12 = request.form['c12']
    #     c13 = request.form['c13']
    #     c14 = request.form['c14']
    #     c23 = request.form['c23']
    #     c24 = request.form['c24']
    #     c34 = request.form['c34']
    #     criteria = Criteria.perbandingan([c12, c13, c14, c23, c24, c34], 4)
    # return render_template('panel/cp_ahp_partai/bobot.html', criteria=criteria, title=title, value=value)