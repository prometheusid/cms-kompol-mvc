from functools import partial
from turtle import title
from sqlalchemy import true
from project import app
from flask import render_template, redirect, url_for, request, session, flash
from project.config.Database import mysql
from flask_mysqldb import MySQLdb
from datetime import datetime
import bcrypt


from project.models.Profile import Profile
from project.models.Anggota import Anggota

@app.route("/dashboard/anggota/<id>")
def cp_anggota(id):
    title = ("ANGGOTA")
    if 'loggedin' in session and session['role'] == 1:
        data = Anggota.semuaAnggota()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN tbl_partai \
                     WHERE users.partai_id = tbl_partai.partai_id ORDER BY users.created_at DESC")
        profile = cur.fetchone()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tbl_partai")
        partaii = cur.fetchall()

        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM tbl_pendidikan")
        edu = edu.fetchall()
        
        return render_template('panel/cp_anggota/index.html', partaii=partaii, data=data, edu=edu, profile=profile, title=title)
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            flash('Silahkan login terlebih dahulu!', 'danger')
            return redirect(url_for('login'))

@app.route("/dashboard/anggota", methods=["GET", "POST"])
def tambahanggota(): 
    if 'loggedin' in session and session['role'] == 1 and 'emailAnggota' in request.form and 'passwordAnggota' in request.form and 'nameAnggota' in request.form: 
        data = Anggota.tambahAnggota()
    return redirect(url_for('cp_anggota', id=id))

@app.route("/dashboard/anggota/<id>", methods=["GET", "POST"])           
def editAnggota(id):
    if 'loggedin' in session and session['role'] == 1:
        data = Anggota.editAnggota(id)
        #return render_template('panel/cp_partai/index.html', title=title)
        return redirect(url_for('cp_anggota', id=id))
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            flash('Silahkan login terlebih dahulu!', 'danger')
            return redirect(url_for('login'))

@app.route("/dashboard/anggota/hapus/<id>")
def hapus_anggota(id):
    if 'loggedin' in session and session['role'] == 1 and session['id']:
        data = Anggota.deleteAnggota(id)
        return redirect(url_for('cp_anggota', id=id))

@app.route("/dashboard/partai/<id>")
def daftar_partai(id):
    title = ("PARTAI")
    if 'loggedin' in session and session['role'] == 1:
        data = Anggota.semuaPartai()

        return render_template('panel/cp_anggota/tambah.html', data=data, title=title)

@app.route("/dashboard/partai", methods=["GET", "POST"])
def cp_tambahpartai():
    if 'loggedin' in session and session['role'] == 1:
        data = Anggota.tambahPartai()
    return redirect(url_for('daftar_partai', id=id))

@app.route("/dashboard/partai/<id>", methods=["GET", "POST"])
def cp_editpartai(id):
    if 'loggedin' in session and session['role'] == 1:
        data = Anggota.editPartai(id)
        return redirect(url_for('daftar_partai', id=id))
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            flash('Silahkan login terlebih dahulu!', 'danger')
            return redirect(url_for('login'))

@app.route("/dashboard/partai/hapus/<id>")
def hapus_partai(id):
    if 'loggedin' in session and session['role'] == 1 and session['id']:
        data = Anggota.deletePartai(id)
        return redirect(url_for('daftar_partai', id=id))