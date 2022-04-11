from project.config.Database import mysql
from datetime import datetime
from flask import request
import ast


class Ahp:
    def fetchValue():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_ahp_partai AS a JOIN tbl_partai as b ON a.partai_id = b.partai_id ORDER BY ahp_partai_id ASC")
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
    
    def addDataCriteria():
        criteria = request.form['criteria']
        c = ast.literal_eval(criteria)
        c12 = c[0][1]
        c13 = c[0][2]
        c14 = c[0][3]
        c23 = c[1][2]
        c24 = c[1][3]
        c34 = c[2][3]

        update_at = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `tbl_criteria_partai` (`c12`, `c13`, `c14`, `c23`, `c24`, `c34`, `update_at`) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (c12, c13, c14, c23, c24, c34, update_at))
        mysql.connection.commit()

