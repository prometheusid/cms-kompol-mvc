from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session

# generate random integer values
from random import seed
from random import randint

class Survey:
    
    def fetchQuestionDPRD():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_survey_question WHERE variabel = 2 ORDER BY created_date ASC")
        data = cur.fetchall()
        return data

    def fetchQuestionPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_survey_question WHERE variabel = 1 ORDER BY created_date ASC")
        data = cur.fetchall()
        return data

    def addDataQuestion():
        code = request.form['code']
        question = request.form['question']
        variabel = request.form['variabel']
        created_date = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `tbl_survey_question` (`code`, `question`, `variabel`, `created_date`) VALUES (%s,%s,%s,%s)",
                    (code, question, variabel, created_date))
        alt = mysql.connection.cursor()
        alt.execute(f"ALTER TABLE `tbl_answer_column` ADD {code} VARCHAR(255) NULL DEFAULT NULL")
        mysql.connection.commit()

    def deleteDataQuestion(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tbl_survey_question WHERE id_survey_question=%s", (id,))
        mysql.connection.commit()

    def fetchDataPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_partai ORDER BY nama_partai ASC")
        data = cur.fetchall()
        return data

    def fetchDataDPRD():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from users WHERE role_id = 3 ORDER BY nama_user ASC")
        data = cur.fetchall()
        return data

    def saveDPRDSurvey():
        user_id_dprd = request.form['id_dprd']
        code_answer = randint(0, 999)

        # Get Question
        id_question1 = request.form['id_question1']
        id_question2 = request.form['id_question2']
        id_question3 = request.form['id_question3']
        id_question4 = request.form['id_question4']
        id_question5 = request.form['id_question5']
        id_question6 = request.form['id_question6']
        id_question7 = request.form['id_question7']
        id_question8 = request.form['id_question8']
        id_question9 = request.form['id_question9']
        id_question10 = request.form['id_question10']

        # Get Answer
        answer1 = request.form['row1']
        answer2 = request.form['row2']
        answer3 = request.form['row3']
        answer4 = request.form['row4']
        answer5 = request.form['row5']
        answer6 = request.form['row6']
        answer7 = request.form['row7']
        answer8 = request.form['row8']
        answer9 = request.form['row9']
        answer10 = request.form['row10']
        
        answer_by = session['id']
        created_date = datetime.now()

        cur = mysql.connection.cursor()
        sql_answer = "INSERT INTO tbl_survey_answer (id_survey_question, code_answer, answer, answer_by, created_date) VALUES (%s, %s, %s, %s, %s)"
        val_answer = [
            (id_question1, code_answer, answer1, answer_by, created_date),
            (id_question2, code_answer, answer2, answer_by, created_date),
            (id_question3, code_answer, answer3, answer_by, created_date),
            (id_question4, code_answer, answer4, answer_by, created_date),
            (id_question5, code_answer, answer5, answer_by, created_date),
            (id_question6, code_answer, answer6, answer_by, created_date),
            (id_question7, code_answer, answer7, answer_by, created_date),
            (id_question8, code_answer, answer8, answer_by, created_date),
            (id_question9, code_answer, answer9, answer_by, created_date),
            (id_question10, code_answer, answer10, answer_by, created_date)
        ]
        
        cur.executemany(sql_answer, val_answer)

        alt = mysql.connection.cursor()
        sql_dprd = "INSERT INTO tbl_survey_dprd (code_answer, user_id_dprd, answer_by) VALUES (%s, %s, %s)"
        val_answer_pil = (code_answer, user_id_dprd, answer_by)

        alt.execute(sql_dprd, val_answer_pil)
        mysql.connection.commit()

    def savePartaiSurvey():
        id_partai = request.form['id_partai']
        code_answer = randint(0, 999)

        # Get Question
        id_question1 = request.form['id_question1']
        id_question2 = request.form['id_question2']
        id_question3 = request.form['id_question3']
        id_question4 = request.form['id_question4']
        id_question5 = request.form['id_question5']
        id_question6 = request.form['id_question6']
        id_question7 = request.form['id_question7']
        id_question8 = request.form['id_question8']
        id_question9 = request.form['id_question9']
        id_question10 = request.form['id_question10']

        # Get Answer
        answer1 = request.form['row1']
        answer2 = request.form['row2']
        answer3 = request.form['row3']
        answer4 = request.form['row4']
        answer5 = request.form['row5']
        answer6 = request.form['row6']
        answer7 = request.form['row7']
        answer8 = request.form['row8']
        answer9 = request.form['row9']
        answer10 = request.form['row10']
        
        answer_by = session['id']
        created_date = datetime.now()

        cur = mysql.connection.cursor()
        sql_answer = "INSERT INTO tbl_survey_answer_partai (id_survey_question, code_answer, answer, answer_by, created_date) VALUES (%s, %s, %s, %s, %s)"
        val_answer = [
            (id_question1, code_answer, answer1, answer_by, created_date),
            (id_question2, code_answer, answer2, answer_by, created_date),
            (id_question3, code_answer, answer3, answer_by, created_date),
            (id_question4, code_answer, answer4, answer_by, created_date),
            (id_question5, code_answer, answer5, answer_by, created_date),
            (id_question6, code_answer, answer6, answer_by, created_date),
            (id_question7, code_answer, answer7, answer_by, created_date),
            (id_question8, code_answer, answer8, answer_by, created_date),
            (id_question9, code_answer, answer9, answer_by, created_date),
            (id_question10, code_answer, answer10, answer_by, created_date)
        ]
        
        cur.executemany(sql_answer, val_answer)

        alt = mysql.connection.cursor()
        sql_dprd = "INSERT INTO tbl_survey_partai (code_answer, id_partai, answer_by) VALUES (%s, %s, %s)"
        val_answer_pil = (code_answer, id_partai, answer_by)

        alt.execute(sql_dprd, val_answer_pil)
        mysql.connection.commit()