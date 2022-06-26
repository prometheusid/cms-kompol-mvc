import profile
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

@app.route("/profile/<id>")
def profileuser(id):
    title = ("PROFILE")
    if 'loggedin' in session:
        profiles = Profile.detaiilProfile(id)
        profileu = Profile.detailProfile(id)
        edu = Profile.eduProfile(id)
        profile = Profile.editProfiles(id)

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
        ahpDewan = CalculateDewan.eigen_dewan(dataAhpDewan, sumDataAhpDewan, valueDewan['rata_eigen'])
        dataPartai = Ahp.fetchValueId(id)
        dataDewan = Ahp.fetchDewanId(id)

        # Pengalaman List
        experiences = Profile.listPengalaman(id)
        return render_template('public/profile/index.html', title=title, profileu=profileu, profile=profile, profiles=profiles, edu=edu, ahpPartai=ahpPartai, dataPartai=dataPartai, ahpDewan=ahpDewan, dataDewan=dataDewan, experiences=experiences)
    return redirect(url_for('login'))

@app.route("/profile/delete/pengalaman/<int:id_pengalaman>/<int:id>")
def deletePengalaman(id_pengalaman, id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tbl_pengalaman WHERE id=%s", (id_pengalaman,))
        mysql.connection.commit()
    return redirect(url_for('profileedit', id=id))

@app.route("/profile/edit/<id>", methods=["GET", "POST"])
def profileedit(id):
    title = ("EDIT PROFILE")
    if request.method == 'GET' and 'loggedin' in session:
        profile = Profile.editProfiles(id)

        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM tbl_pendidikan")
        edu = edu.fetchall()

        edus = mysql.connection.cursor()
        edus.execute("SELECT * FROM tbl_pendidikan LEFT JOIN users ON tbl_pendidikan.id_pendidikan=users.id_pendidikan WHERE users.user_id=%s", [id])
        edus = edus.fetchall()

        experiences = Profile.listPengalaman(id)
        return render_template('public/profile/editprofile.html', edus=edus, edu=edu, profile=profile, experiences=experiences, title=title)
    elif 'loggedin' in session:
        idu = request.form['idu']
        name = request.form['name']
        update = datetime.now()
        education = request.form['education']
        # pengalaman = request.form['pengalaman']
        twitter = request.form['twitter']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nama_user = %s, updated_at = %s, id_pendidikan = %s, akun_twitter = %s WHERE user_id = %s",
                    (name, update, education, twitter, idu))
        
        # Pengalaman
        cur.execute("DELETE FROM tbl_pengalaman WHERE user_id=%s", (id,))
        experience = request.form.getlist('experience[]')
        for value in experience:  
            cur.execute("INSERT INTO tbl_pengalaman (user_id, pengalaman, created_at, updated_at) VALUES (%s, %s, %s, %s)",[id, value, update, update])       
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('profileedit', id=id))
    return redirect(url_for('login'))