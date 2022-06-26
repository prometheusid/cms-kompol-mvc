from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# Import models
from project.models.Rekomendasi import Rekomendasi

# Detail Info
@app.route('/rekomendasi/detail/<int:id>')
def detai_rekomendasi(id):
    title = ("Rekomendasi Partai")
    data = Rekomendasi.detail(id)
    return render_template('public/rekomendasi/index.html', data=data, title=title)