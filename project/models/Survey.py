from project import app
from project.config.Database import mysql
from datetime import datetime

class Survey:
    
    def fetchQuestion():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_survey_question ORDER BY created_date DESC")
        data = cur.fetchall()
        return data