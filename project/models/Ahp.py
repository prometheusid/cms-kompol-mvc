from project.config.Database import mysql
from datetime import datetime
from flask import request
import ast


class Ahp:
    def fetchValue():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_ahp_partai AS a JOIN tbl_partai as b ON a.partai_id = b.partai_id ORDER BY a.partai_id ASC")
        data = cur.fetchall()
        return data
    
    def fetchValueDewan():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_ahp_dprd AS a JOIN users as b ON a.user_id = b.user_id ORDER BY a.user_id ASC")
        data = cur.fetchall()
        return data
    
    def sumValue():
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(komunikator_jumlah) as jml_c1, SUM(komunikator_sentiment) as sentiment_c1, SUM(popularitas_eksistensi) as eksi_c2, SUM(popularitas_citra) as citra_c2, SUM(laporan_jumlah) as jml_c3, SUM(laporan_sentiment) as sentiment_c3, SUM(integritas_jumlah) as jml_c4, SUM(integritas_sentiment) as sentiment_c4 from tbl_ahp_partai")
        data = cur.fetchall()
        return data
    
    def sumValueDewan():
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(kompetensi_akademik) as kompetensi_c1, SUM(kompetensi_experience) as experience_c1, SUM(popularitas_eksistensi) as eksi_c2, SUM(popularitas_citra) as citra_c2, SUM(forum_jumlah) as jml_c3, SUM(forum_sentiment) as sentiment_c3, SUM(laporan_jumlah) as jml_c4, SUM(laporan_sentiment) as sentiment_c4, SUM(integritas_jumlah) as jml_c5, SUM(integritas_sentiment) as sentiment_c5 from tbl_ahp_dprd")
        data = cur.fetchall()
        return data
    
    def matrixPartai(nilai):
        data = {}
        data["nilai"] = nilai
        data["tambahan"] = 10
        return data
    
    def fetchCriteriaPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_criteria_partai WHERE id = 1 ")
        data = cur.fetchone()
        return data

    def fetchCriteriaDewan():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_criteria_dprd WHERE id = 1 ")
        data = cur.fetchone()
        return data
    
    def updateDataCriteriaPartai():
        criteria = request.form['criteria']
        c = ast.literal_eval(criteria)
        c12 = c[0][1]
        c13 = c[0][2]
        c14 = c[0][3]
        c23 = c[1][2]
        c24 = c[1][3]
        c34 = c[2][3]

        updated_at = datetime.now()
        update = mysql.connection.cursor()
        sql_update = "UPDATE tbl_criteria_partai SET c12 = %s, c13 = %s, c14 = %s, c23 = %s, c24 = %s, c34 = %s, updated_at = %s  WHERE id = 1"
        value = (c12, c13, c14, c23, c24, c34, updated_at)
        update.execute(sql_update, value)
        mysql.connection.commit()
    
    def updateDataCriteriaDewan():
        criteria = request.form['criteria']
        c = ast.literal_eval(criteria)
        c12 = c[0][1]
        c13 = c[0][2]
        c14 = c[0][3]
        c15 = c[0][4]
        c23 = c[1][2]
        c24 = c[1][3]
        c25 = c[1][4]
        c34 = c[2][3]
        c35 = c[2][4]
        c45 = c[3][4]

        updated_at = datetime.now()
        update = mysql.connection.cursor()
        sql_update = "UPDATE tbl_criteria_dprd SET c12 = %s, c13 = %s, c14 = %s, c15 = %s, c23 = %s, c24 = %s, c25 = %s, c34 = %s, c35 = %s, c45 = %s, updated_at = %s  WHERE id = 1"
        value = (c12, c13, c14, c15, c23, c24, c25, c34, c35, c45, updated_at)
        update.execute(sql_update, value)
        mysql.connection.commit()

