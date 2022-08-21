
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# generate random integer values
from random import seed
from random import randint

# Import models
from project.models.Survey import Survey
from project.models.GenerateAhpDewan import GenerateAhpDewan
from project.models.GenerateAhpPartai import GenerateAhpPartai

#route index
@app.route("/dashboard/survey/question")
def cp_survey():
    title = ("Data Survey")
    # fetch data from model
    value = "q"+str(randint(0, 999))
    data = Survey.fetchQuestionDPRD()
    return render_template('panel/cp_survey/index.html', data=data, value=value, title=title)

@app.route("/dashboard/survey/question/partai")
def cp_survey_partai():
    title = ("Data Survey")
    # fetch data from model
    value = "q"+str(randint(0, 999))
    data = Survey.fetchQuestionPartai()
    return render_template('panel/cp_survey/index2.html', data=data, value=value, title=title)

@app.route("/survey/tambah-question", methods=["GET", "POST"])
def cp_survey_question():
    data = Survey.addDataQuestion()
    return redirect(url_for('cp_survey'))

@app.route("/survey/delete/<int:id>")
def hapus_survey(id):
    data = Survey.deleteDataQuestion(id)
    return redirect(url_for('cp_survey'))

# Route berdasarkan data dewan
@app.route("/dashboard/survey/result/dewan")
def cp_result_dewan():
    title = ("Data Survey Dewan")
    data = Survey.countSurveyDPRD()
    return render_template('panel/cp_survey/result.html', data=data, title=title)

@app.route("/dashboard/survey/result/partai")
def cp_result_partai():
    title = ("Data Survey Partai")
    data = Survey.countSurveyPartai()
    return render_template('panel/cp_survey/result2.html', data=data, title=title)

# Generate survey dewan
@app.route("/dashboard/survey/dewan/generate", methods=["POST"])
def cp_survey_dewan_generate():
    GenerateAhpDewan.updateIntegritas()
    GenerateAhpDewan.updateJumlahLapkun()
    GenerateAhpDewan.updateSentimentLapkun()
    GenerateAhpDewan.updateForum()
    GenerateAhpDewan.updateKompetensiAkademik()
    GenerateAhpDewan.updateKompetensiExperience()
    GenerateAhpDewan.updateSurvey() 
    return redirect(url_for('cp_result_dewan'))

# Generate survey partai
@app.route("/dashboard/survey/partai/generate", methods=["POST"])
def cp_survey_partai_generate():
    GenerateAhpPartai.updateSurvey()
    GenerateAhpPartai.updateJumlahLapkun()
    GenerateAhpPartai.updateSentimentLapkun()
    GenerateAhpPartai.updateIntegritas()
    GenerateAhpPartai.updateKomunikator()
    return redirect(url_for('cp_result_partai'))
