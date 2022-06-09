from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session
from flask_mysqldb import MySQLdb

# generate random integer values
from random import seed
from random import randint

class Dashboard:

    def getUsers(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_id=%s", (id,))
        user = cur.fetchone()
        return user

    def countDprd():
        cur = mysql.connection.cursor()
        cur.execute("SELECT role_id, COUNT('role_id') as jumlah_dprd FROM users WHERE role_id = 3")
        data = cur.fetchone()
        return data
    
    def countPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT('partai_id') as jumlah_partai FROM tbl_partai")
        data = cur.fetchone()
        return data

    def countWarga():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT('role_id') as jumlah_warga FROM users WHERE role_id = 4")
        data = cur.fetchone()
        return data

    def countInfo():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT('info_id') as jumlah_info FROM info")
        data = cur.fetchone()
        return data