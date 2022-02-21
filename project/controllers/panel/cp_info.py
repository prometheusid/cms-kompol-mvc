from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""
# Import models
from project.models.Info import Info

@app.route('/dashboard/cp_info')
def cp_info():
    title = ('INFO PUBLIK')
    data = Info.fetchInfo()
    return render_template('panel/cp_info/index.html', data=data, title=title)


@app.route("/dashboard/cp_info/delete/<int:id>")
def hapus_info(id):
    data = Info.deleteDataInfo(id)
    return redirect(url_for('cp_info'))