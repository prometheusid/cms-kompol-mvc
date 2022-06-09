from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os

class Anggota:

    def deleteAnggota(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", [id])
        mysql.connection.commit()

    def deleteAnggotaPartai(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", [id])
        mysql.connection.commit()