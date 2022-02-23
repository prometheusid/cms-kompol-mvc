from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# generate random integer values
from random import seed
from random import randint

# Import models
from project.models.Survey import Survey


# #route index

# 1. index untuk menampilkan data keseluruhan
# 2. create untuk tombol memlih create/or function dll.
# 3. store create/add from database(menyimpan)
# 4. show (menampilkan satu bagian)
# 5. edit (untuk redirect tombol edit)
# 6. update (untuk update data yg baru)
# 7. destroy (hapus)

@app.route("/dashboard/ahp/dewan")
def cp_ahp_dewan():
    return "Sedang dibuat sabar dan kalem wak"

# @app.route("/survey/tambah-question", methods=["GET", "POST"])
# def cp_survey_question():
#     data = Survey.addDataQuestion()
#     return redirect(url_for('cp_survey'))