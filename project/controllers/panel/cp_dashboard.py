from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""
# dashboard / cpanel admin
@app.route("/dashboard")
def dashboard():
    user_role = session.get('role')
    if user_role == 0:
        return render_template('panel/cp_dashboard/index.html')
    else:
        return redirect(url_for('pub_home'))
