from project.config.Database import mysql
from datetime import datetime
from flask import request


class Ahp:
    def fetchValue():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_ahp_partai AS a JOIN tbl_partai as b ON a.partai_id = b.partai_id ORDER BY ahp_partai_id ASC")
        data = cur.fetchall()
        return data
    
    def matrixPartai(nilai):
        # https://www.w3schools.com/python/python_dictionaries.asp
        data = {}
        data["nilai"] = nilai
        data["tambahan"] = 10
        return data
    
    def fetchCriteriaPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_criteria_partai WHERE id = 1 ")
        data = cur.fetchone()
        return data
