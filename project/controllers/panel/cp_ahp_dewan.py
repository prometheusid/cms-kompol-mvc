from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# Import models
from project.models.Ahp import Ahp
from project.models.CalculateDewan import CalculateDewan
from project.models.Criteria import Criteria


@app.route("/dashboard/ahp/dewan")
def cp_ahp_dewan():
    title = ("Ahp Dewan")
    criteria = Ahp.fetchCriteriaDewan()
    value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c15'], criteria['c23'], criteria['c24'], criteria['c25'], criteria['c34'], criteria['c35'], criteria['c45']], 5)
    dataAhpDewan = Ahp.fetchValueDewan()
    sumDataAhpDewan = Ahp.sumValueDewan()
    data = CalculateDewan.eigen_dewan(dataAhpDewan, sumDataAhpDewan, value['rata_eigen'])
    return render_template('panel/cp_ahp_dewan/index.html', data=data, title=title)

@app.route("/dashboard/ahp/bobot/dewan", methods=["GET", "POST"])
def cp_ahp_bobot_dewan():
    title = ("Ahp bobot")
    ahp = Ahp.fetchCriteriaDewan()
    value = Criteria.perbandingan([ahp['c12'], ahp['c13'], ahp['c14'], ahp['c15'], ahp['c23'], ahp['c24'], ahp['c25'], ahp['c34'], ahp['c35'], ahp['c45']], 5)
    criteria = ""
    if (request.form) :
        c12 = request.form['c12']
        c13 = request.form['c13']
        c14 = request.form['c14']
        c15 = request.form['c15']
        c23 = request.form['c23']
        c24 = request.form['c24']
        c25 = request.form['c25']
        c34 = request.form['c34']
        c35 = request.form['c35']
        c45 = request.form['c45']
        criteria = Criteria.perbandingan([c12, c13, c14, c15, c23, c24, c25, c34, c35, c45], 5)
    return render_template('panel/cp_ahp_dewan/bobot.html', criteria=criteria, title=title, value=value)

@app.route("/dashboard/ahp/bobot/dewan/save", methods=["POST"])
def cp_ahp_bobot_dewan_save():
    title = ("Ahp bobot")
    save = Ahp.updateDataCriteriaDewan()
    ahp = Ahp.fetchCriteriaDewan()
    value = Criteria.perbandingan([ahp['c12'], ahp['c13'], ahp['c14'], ahp['c15'], ahp['c23'], ahp['c24'], ahp['c25'], ahp['c34'], ahp['c35'], ahp['c45']], 5)
    criteria = ""
    return render_template('panel/cp_ahp_dewan/bobot.html', criteria=criteria, title=title, value=value)