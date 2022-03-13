from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os

class LaporanKunjungan:

    def fetchKunjungan3():
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM tbl_lapkun as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC LIMIT 3")
        data = cur.fetchall()
        return data