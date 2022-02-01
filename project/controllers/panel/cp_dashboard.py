from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""
# dashboard / cpanel admin
@app.route("/dashboard/<id>")
def dashboard(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=%s", (id,))
    user = cur.fetchone()
    return render_template('panel/cp_dashboard/index.html', user=user)