from flask_login import login_required
from project import app
from flask import render_template, redirect, url_for, request
from datetime import datetime
from project.config.Database import mysql
import bcrypt
from ..auth.auth import session

# Import models
from project.models.Profile import Profile

from project.models.Ahp import Ahp
from project.models.Calculate import Calculate
from project.models.Criteria import Criteria
from project.models.CalculateDewan import CalculateDewan

@app.route("/profile/<name>")
def profileuser(name):
    title = ("PROFILE")
    if 'loggedin' in session:
        profiles = Profile.detaiilProfile(name)
        edu = Profile.eduProfile(name)

        # AHP PARTAI
        criteria = Ahp.fetchCriteriaPartai()
        value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c23'], criteria['c24'], criteria['c34']], 4)
        dataAhpPartai = Ahp.fetchValue()
        sumDataAhpPartai = Ahp.sumValue()
        ahpPartai = Calculate.eigen_partai(dataAhpPartai, sumDataAhpPartai, value['rata_eigen'])
        
        # AHP DEWAN
        criteriaDewan = Ahp.fetchCriteriaDewan()
        valueDewan = Criteria.perbandingan([criteriaDewan['c12'], criteriaDewan['c13'], criteriaDewan['c14'], criteriaDewan['c15'], criteriaDewan['c23'], criteriaDewan['c24'], criteriaDewan['c25'], criteriaDewan['c34'], criteriaDewan['c35'], criteriaDewan['c45']], 5)
        dataAhpDewan = Ahp.fetchValueDewan()
        sumDataAhpDewan = Ahp.sumValueDewan()
        ahpDewan = CalculateDewan.eigen_partai(dataAhpDewan, sumDataAhpDewan, valueDewan['rata_eigen'])
        dataPartai = Ahp.fetchValueId(name)
        dataDewan = Ahp.fetchDewanId(name)
        return render_template('public/profile/index.html', title=title, profiles=profiles, edu=edu, ahpPartai=ahpPartai, dataPartai=dataPartai, ahpDewan=ahpDewan, dataDewan=dataDewan)
    return redirect(url_for('login'))

@app.route("/profile/edit/<name>", methods=["GET", "POST"])
def profileedit(name):
    title = ("EDIT PROFILE")
    if request.method == 'GET' and 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN role_users ON role_users.role_id=users.role_id \
                    JOIN tbl_partai ON tbl_partai.partai_id=users.partai_id WHERE users.user_id=%s", (name,))
        profile = cur.fetchone()

        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM tbl_pendidikan")
        edu = edu.fetchall()
        return render_template('public/profile/editprofile.html', edu=edu, profile=profile, title=title)
    elif 'loggedin' in session:
        idu = request.form['idu']
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        update = datetime.now()
        education = request.form['education']
        pengalaman = request.form['pengalaman']
        twitter = request.form['twitter']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nama_user = %s, password = %s, updated_at = %s, id_pendidikan = %s, pengalaman = %s, akun_twitter = %s WHERE user_id = %s",
                    (name, hash_password, update, education, pengalaman, twitter, idu))
        mysql.connection.commit()
        return redirect(url_for('profileuser', name=name))
    return redirect(url_for('login'))