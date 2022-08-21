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

class DashboardPartai:

    def countDprd(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT role_id, COUNT('role_id') as jumlah_dprd FROM users WHERE role_id = 3 AND partai_id=%s", (id,))
        data = cur.fetchone()
        return data

    def countSurvey(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT('id_partai') as jumlah \
            FROM tbl_survey_partai \
            WHERE id_partai = %s \
            GROUP BY id_partai", (id,))
        data = cur.fetchone()

        if data == None:
            return 0
        else:
            return data['jumlah']

    def countKunjungan(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(B.partai_id) as jumlah\
            from tbl_lapkun as A \
            JOIN users as B \
            ON A.user_id = B.user_id\
            WHERE B.partai_id = %s \
            GROUP BY B.partai_id ", (id,))
        data = cur.fetchone()

        if data == None:
            return 0
        else:
            return data['jumlah']
    
    def countAhpPartai(id): # id adalah partai_id
        criteria = Ahp.fetchCriteriaPartai()
        value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c23'], criteria['c24'], criteria['c34']], 4)
        dataAhpPartai = Ahp.fetchValue()
        sumDataAhpPartai = Ahp.sumValue()
        data = Calculate.eigen_partai(dataAhpPartai, sumDataAhpPartai, value['rata_eigen'])

        
        dataScore = []
        for item in data:
            dataScore.append({'nama_partai' : item['nama_partai'],'partai_id' : item['partai_id'], 'score' : item['value'][4], 'value' : item['value']});
        newlist = sorted(dataScore, key=lambda k: k['score'], reverse=True)

        ranking = []
        for idx, x in enumerate(newlist):
            if x['partai_id'] == id:
                ranking.append({'nama_partai' : x['nama_partai'], 'partai_id' : x['partai_id'], 'score' : x['score'], 'ranking' : idx + 1, 'value' : x['value']});
        return ranking

    def lapkun(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(B.partai_id) as jumlah_kunjungan \
            from tbl_lapkun as A \
            JOIN users as B \
            ON A.user_id = B.user_id\
            WHERE B.partai_id = %s \
            GROUP BY B.partai_id ", (id,))
        lapkun = cur.fetchone()

        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(C.lapkun_id) as jumlah_komentar\
            from tbl_lapkun as A \
            JOIN users as B \
            ON A.user_id = B.user_id\
            LEFT JOIN tbl_detail_lapkun as C \
            ON A.lapkun_id = C.lapkun_id \
            WHERE B.partai_id = %s \
            GROUP BY B.partai_id ", (id,))
        komentar = cur.fetchone()
        
        data = []
        data.append({'jumlah_kunjungan' : lapkun['jumlah_kunjungan'], 'jumlah_komentar' : komentar['jumlah_komentar']});
        return data[0]
    
    def sentimentLapkun(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT laporan_sentiment\
            from tbl_ahp_partai \
            WHERE partai_id = %s", (id,))
        data = cur.fetchone()
        return data
    
    def lapkunDewan(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT B.user_id, COUNT(C.lapkun_id) as jumlah_komentar\
            from tbl_lapkun as A \
            JOIN users as B \
            ON A.user_id = B.user_id\
            LEFT JOIN tbl_detail_lapkun as C \
            ON A.lapkun_id = C.lapkun_id \
            WHERE B.partai_id = %s \
            GROUP BY B.user_id \
            ORDER BY B.user_id ASC", (id,))
        komentar = cur.fetchall()

        cur.execute("SELECT B.nama_user, B.user_id, COUNT(A.lapkun_id) as jumlah_kunjungan, C.laporan_sentiment \
            from tbl_lapkun as A \
            JOIN users as B \
            ON A.user_id = B.user_id\
            JOIN tbl_ahp_dprd as C \
            ON B.user_id = C.user_id\
            WHERE B.partai_id = %s \
            GROUP BY B.user_id \
            ORDER BY B.user_id ASC", (id,))
        lapkun = cur.fetchall()

        data = []
        for i in range(len(lapkun)):
            data.append({'nama' : lapkun[i]['nama_user'], 'jumlah_kunjungan' : lapkun[i]['jumlah_kunjungan'], 'sentiment' : lapkun[i]['laporan_sentiment'], 'jumlah_komentar' : komentar[i]['jumlah_komentar']});

        return data

    def countSurveyDewan(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT A.nama_user, COUNT(B.user_id_dprd) as jumlah, C.popularitas_eksistensi as eksistensi, C.popularitas_citra as citra\
            FROM users as A \
            LEFT JOIN tbl_survey_dprd as B \
            ON A.user_id = B.user_id_dprd \
            JOIN tbl_ahp_dprd as C\
            ON A.user_id = C.user_id\
            WHERE A.partai_id =%s AND role_id=3\
            GROUP BY A.user_id", (id,))   
        data = cur.fetchall()
        return data 
    
    def countSurveyPartai(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(C.id_partai) as jumlah, B.popularitas_eksistensi as eksistensi, B.popularitas_citra as citra \
            FROM tbl_ahp_partai as B \
            LEFT JOIN tbl_survey_partai as C \
            ON C.id_partai = B.partai_id \
            WHERE B.partai_id =%s", (id,))
        data = cur.fetchone()
        return data 

    def countAhpDewan(id): # id adalah partai_id
        criteria = Ahp.fetchCriteriaDewan()
        value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c15'], criteria['c23'], criteria['c24'], criteria['c25'], criteria['c34'], criteria['c35'], criteria['c45']], 5)
        dataAhpDewan = Ahp.fetchValueDewanByPartaiId(id)
        sumDataAhpDewan = Ahp.sumValueDewan()
        data = CalculateDewan.eigen_dewan(dataAhpDewan, sumDataAhpDewan, value['rata_eigen'])
        return data
    
    def countPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(partai_id) as jumlah\
            from tbl_partai")
        data = cur.fetchone()
        return data

    def getKomunikatorPartaiById(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT a.partai_id, a.nama_partai, a.head_leader, a.account_head_leader, COUNT('b.partai_id') as jumlah_tweet \
            from tbl_partai as a \
            JOIN tbl_crawling_komunikator_partai as b \
            ON a.partai_id = b.partai_id \
            WHERE a.partai_id = %s \
            GROUP BY b.partai_id \
            ORDER BY a.partai_id ASC", (id,)) 
        data = cur.fetchall()
        return data
    
    def getIntegritasPartaiById(id): # id adalah partai_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT a.partai_id, a.nama_partai, a.head_leader, a.account_twitter, COUNT('b.partai_id') as jumlah_tweet \
            from tbl_partai as a \
            JOIN tbl_crawling_integritas_partai as b \
            ON a.partai_id = b.partai_id \
            WHERE a.partai_id = %s \
            GROUP BY b.partai_id \
            ORDER BY a.partai_id ASC", (id,)) 
        data = cur.fetchall()
        return data
    
    def getAllDataIntegritasPartaiById(id): # id adalah partai_id
        cur = mysql.connection.cursor() 
        cur.execute("SELECT tweet \
            from tbl_crawling_integritas_partai \
            WHERE partai_id = %s \
            ORDER BY created_at DESC", (id,)) 
        data = cur.fetchall()
        return data
    
    def getAllDataKomunikatorPartaiById(id): # id adalah partai_id
        cur = mysql.connection.cursor() 
        cur.execute("SELECT A.id, A.tweet, B.head_leader \
            from tbl_crawling_komunikator_partai as A \
            JOIN tbl_partai as B ON A.partai_id = B.partai_id \
            WHERE A.partai_id = %s \
            ORDER BY A.created_at DESC", (id,)) 
        data = cur.fetchall()
        return data