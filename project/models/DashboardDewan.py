from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session
from flask_mysqldb import MySQLdb
import os

# generate random integer values
from random import seed
from random import randint

from project.models.Ahp import Ahp
from project.models.Calculate import Calculate
from project.models.Criteria import Criteria
from project.models.GenerateAhpPartai import GenerateAhpPartai
from project.models.CalculateDewan import CalculateDewan
from project.models.GenerateAhpDewan import GenerateAhpDewan

class DashboardDewan:
    def countTweet(id): # user_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(user_id) jumlah_tweet \
            from tbl_crawling_integritas_dprd \
            WHERE user_id = %s \
            ORDER BY created_at DESC", (id,)) 
        data = cur.fetchone()
        return data
    
    def countSurvey(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT('id_survey_dprd') as jumlah \
            FROM tbl_survey_dprd \
            WHERE user_id_dprd = %s", (id,))
        data = cur.fetchone()

        if data == None:
            return 0
        else:
            return data['jumlah']
    
    def countKunjungan(id): # id adalah user_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(lapkun_id) as jumlah\
            from tbl_lapkun \
            WHERE user_id = %s", (id,))
        data = cur.fetchone()

        if data == None:
            return 0
        else:
            return data['jumlah']

    def countAhpDewan(id): # id adalah user_id
        criteria = Ahp.fetchCriteriaDewan()
        value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c15'], criteria['c23'], criteria['c24'], criteria['c25'], criteria['c34'], criteria['c35'], criteria['c45']], 5)
        dataAhpDewan = Ahp.fetchValueDewan()
        sumDataAhpDewan = Ahp.sumValueDewan()
        data = CalculateDewan.eigen_dewan(dataAhpDewan, sumDataAhpDewan, value['rata_eigen'])

        dataScore = []
        for item in data:
            dataScore.append({'user_id' : item['user_id'], 'score' : item['value'][5], 'value' : item['value']});
        newlist = sorted(dataScore, key=lambda k: k['score'], reverse=True)

        ranking = []
        for idx, x in enumerate(newlist):
            if x['user_id'] == id:
                ranking.append({'user_id' : x['user_id'], 'score' : x['score'], 'ranking' : idx + 1, 'value' : x['value']});
        return ranking

    def lapkunDewan(id): # id adalah user_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT A.user_id, COUNT(C.lapkun_id) as jumlah_komentar\
            from tbl_lapkun as A \
            LEFT JOIN tbl_detail_lapkun as C \
            ON A.lapkun_id = C.lapkun_id \
            WHERE A.user_id = %s \
            GROUP BY A.user_id \
            ORDER BY A.user_id ASC", (id,))
        komentar = cur.fetchone()
        if komentar == None:
            jumlahKomentar = 0
        else:
            jumlahKomentar = komentar['jumlah_komentar']

        cur.execute("SELECT A.user_id, COUNT(A.lapkun_id) as jumlah_kunjungan, C.laporan_sentiment \
            from tbl_lapkun as A \
            JOIN tbl_ahp_dprd as C \
            ON A.user_id = C.user_id\
            WHERE A.user_id =  %s\
            GROUP BY A.user_id \
            ORDER BY A.user_id ASC", (id,))
        lapkun = cur.fetchone()

        if lapkun == None:
            jumlahKunjungan = 0
            laporanSentiment = 0
        else:
            jumlahKunjungan = lapkun['jumlah_kunjungan']
            laporanSentiment = lapkun['laporan_sentiment']
    
        data = []
        data.append({'jumlah_kunjungan' : jumlahKunjungan, 'sentiment' : laporanSentiment, 'jumlah_komentar' : jumlahKomentar});
        return data

    def fetchLapkun(id): # id adalah user_id
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * \
            FROM tbl_lapkun \
            WHERE user_id = %s \
            ORDER BY created_at DESC", (id,))
        data = cur.fetchall()
        return data

    def countSurveyDewan(id): #id adalah user_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(B.user_id_dprd) as jumlah, C.popularitas_eksistensi as eksistensi, C.popularitas_citra as citra\
            FROM users as A \
            LEFT JOIN tbl_survey_dprd as B \
            ON A.user_id = B.user_id_dprd \
            JOIN tbl_ahp_dprd as C\
            ON A.user_id = C.user_id\
            WHERE A.user_id =%s AND role_id=3\
            GROUP BY A.user_id", (id,))   
        data = cur.fetchall()
        return data 

    def countAhpDewan(id): # id adalah partai_id
        criteria = Ahp.fetchCriteriaDewan()
        value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c15'], criteria['c23'], criteria['c24'], criteria['c25'], criteria['c34'], criteria['c35'], criteria['c45']], 5)
        dataAhpDewan = Ahp.fetchValueDewanByPartaiId(id)
        sumDataAhpDewan = Ahp.sumValueDewan()
        data = CalculateDewan.eigen_dewan(dataAhpDewan, sumDataAhpDewan, value['rata_eigen'])
        return data
# a