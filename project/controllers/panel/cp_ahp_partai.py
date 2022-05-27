from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

from project.models.Ahp import Ahp
from project.models.Calculate import Calculate
from project.models.Criteria import Criteria
from project.models.GenerateAhpPartai import GenerateAhpPartai

@app.route("/dashboard/ahp/partai")
def cp_ahp_partai():
    title = ("Ahp Partai")
    criteria = Ahp.fetchCriteriaPartai()
    value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c23'], criteria['c24'], criteria['c34']], 4)
    dataAhpPartai = Ahp.fetchValue()
    sumDataAhpPartai = Ahp.sumValue()
    data = Calculate.eigen_partai(dataAhpPartai, sumDataAhpPartai, value['rata_eigen'])
    return render_template('panel/cp_ahp_partai/index.html', data=data, title=title)

@app.route("/dashboard/ahp/bobot/partai", methods=["GET", "POST"])
def cp_ahp_bobot_partai():
    title = ("Ahp bobot")
    ahp = Ahp.fetchCriteriaPartai()
    value = Criteria.perbandingan([ahp['c12'], ahp['c13'], ahp['c14'], ahp['c23'], ahp['c24'], ahp['c34']], 4)
    criteria = ""
    if (request.form) :
        c12 = request.form['c12']
        c13 = request.form['c13']
        c14 = request.form['c14']
        c23 = request.form['c23']
        c24 = request.form['c24']
        c34 = request.form['c34']
        criteria = Criteria.perbandingan([c12, c13, c14, c23, c24, c34], 4)
    return render_template('panel/cp_ahp_partai/bobot.html', criteria=criteria, title=title, value=value)

@app.route("/dashboard/ahp/bobot/partai/save", methods=["POST"])
def cp_ahp_bobot_partai_save():
    title = ("Ahp bobot")
    save = Ahp.updateDataCriteriaPartai()
    ahp = Ahp.fetchCriteriaPartai()
    value = Criteria.perbandingan([ahp['c12'], ahp['c13'], ahp['c14'], ahp['c23'], ahp['c24'], ahp['c34']], 4)
    criteria = ""
    return render_template('panel/cp_ahp_partai/bobot.html', criteria=criteria, title=title, value=value)

@app.route("/dashboard/ahp/partai/generate")
def cp_ahp_partai_generate():
    data = GenerateAhpPartai.updateKomunikator()
    return str(data)
