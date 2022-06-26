import re
from project.config.Database import mysql
from datetime import datetime

from project.models.Crawling import Crawling
from project.models.Sentiment import Sentiment

from operator import itemgetter
from itertools import groupby
from functools import partial

class GenerateAhpDewan:
    def valueSentiment(value):
        if (value >= 90):
            point = 100
        if (value >= 85 and value <= 89):
            point = 95
        if (value >= 80 and value <= 84):
            point = 90  
        if (value >= 70 and value <= 79):
            point = 85 
        if (value >= 60 and value <= 69):
            point = 80 
        if (value >= 55 and value <= 59):
            point = 75
        if (value >= 50 and value <= 54):
            point = 70
        if (value >= 40 and value <= 49):
            point = 60 
        if (value >= 30 and value <= 39):
            point = 55  
        if (value >= 20 and value <= 29):
            point = 50
        if (value >= 10 and value <= 19):
            point = 40
        if (value >= 0 and value <= 9):
            point = 30
        return point
    
    def valueKompetensiAkademik(pendidikanId):
        if (pendidikanId == 10):
            point = 100
        if (pendidikanId == 9):
            point = 90
        if (pendidikanId == 8 or pendidikanId == 7):
            point = 70
        if (pendidikanId <= 6 and pendidikanId >= 4):
            point = 60
        if (pendidikanId == 3 or pendidikanId == 2):
            point = 50
        if (pendidikanId == 1):
            point = 30
        return point

    def updateIntegritas(): 
        tweetIntegritas = Crawling.getTweetIntegritasDprd()
        sentimentIntegritas = Sentiment.predictDprd(tweetIntegritas)
    
        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in sentimentIntegritas:
            integritasJumlah = item['total_positive'] + item['total_negative']
            integritasSentiment = (item['total_positive'] / (item['total_positive'] + item['total_negative'])) * 100
            pointIntegritasSentiment = GenerateAhpDewan.valueSentiment(integritasSentiment)

            sql_update = "UPDATE tbl_ahp_dprd SET integritas_jumlah = %s, integritas_sentiment = %s, updated_at = %s WHERE user_id = %s"
            value = (integritasJumlah, pointIntegritasSentiment , updatedAt, item['user_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
        return "berhasil"

    def updateJumlahLapkun():
        connect = mysql.connection.cursor()
        connect.execute("SELECT COUNT(user_id) as jumlah, user_id FROM tbl_lapkun GROUP BY user_id")
        lapkun = connect.fetchall() 

        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in lapkun:
            sql_update = "UPDATE tbl_ahp_dprd SET laporan_jumlah = %s, updated_at = %s WHERE user_id = %s"
            value = (item['jumlah'], updatedAt, item['user_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
        return "berhasil"

    def updateSentimentLapkun():
        connect = mysql.connection.cursor()
        connect.execute("SELECT A.lapkun_id, A.user_id, B.komentar as tweet FROM tbl_lapkun as A JOIN tbl_detail_lapkun as B ON A.lapkun_id = B.lapkun_id")
        lapkun = connect.fetchall()
    
        data = Sentiment.predictLapkunDewan(lapkun)

        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in data:
            laporanSentiment = (item['total_positive'] / (item['total_positive'] + item['total_negative'])) * 100
            pointLaporanSentiment = GenerateAhpDewan.valueSentiment(laporanSentiment)

            sql_update = "UPDATE tbl_ahp_dprd SET laporan_sentiment = %s, updated_at = %s WHERE user_id = %s"
            value = (pointLaporanSentiment, updatedAt, item['user_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
        return "berhasil"
    
    def updateForum():
        connect = mysql.connection.cursor()
        connect.execute("SELECT A.user_id, A.forum_id, B.komentar as tweet FROM tbl_forum as A JOIN tbl_detail_forum as B ON A.forum_id = B.forum_id JOIN users as C ON A.user_id = C.user_id WHERE C.role_id = 3")
        forum = connect.fetchall()

        data = Sentiment.predictForumDewan(forum)
        
        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in data:
            forumJumlah = item['total_positive'] + item['total_negative']
            forumSentiment = (item['total_positive'] / (item['total_positive'] + item['total_negative'])) * 100
            pointForumSentiment = GenerateAhpDewan.valueSentiment(forumSentiment)

            sql_update = "UPDATE tbl_ahp_dprd SET forum_jumlah = %s, forum_sentiment = %s, updated_at = %s WHERE user_id = %s"
            value = (forumJumlah, pointForumSentiment, updatedAt, item['user_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
        return "berhasil"
    
    def updateKompetensiAkademik():
        connect = mysql.connection.cursor()
        connect.execute("SELECT * FROM users WHERE role_id = 3")
        kompetensi = connect.fetchall()

        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in kompetensi:
            kompetensiAkademik = GenerateAhpDewan.valueKompetensiAkademik(item['id_pendidikan'])
            sql_update = "UPDATE tbl_ahp_dprd SET kompetensi_akademik = %s, updated_at = %s WHERE user_id = %s"
            value = (kompetensiAkademik, updatedAt, item['user_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
        return "berhasil"
    
    def updateKompetensiExperience():
        connect = mysql.connection.cursor()
        connect.execute("SELECT COUNT(user_id) as jumlah, user_id FROM tbl_pengalaman GROUP BY user_id")
        experience = connect.fetchall()

        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in experience:
            sql_update = "UPDATE tbl_ahp_dprd SET kompetensi_experience = %s, updated_at = %s WHERE user_id = %s"
            value = (item['jumlah'], updatedAt, item['user_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
        return "berhasil"
    
    def updateSurvey():
        connect = mysql.connection.cursor()
        connect.execute("SELECT A.user_id_dprd as user_id, A.code_answer, B.id_survey_question, B.answer FROM tbl_survey_dprd as A JOIN tbl_survey_answer as B ON A.code_answer = B.code_answer")
        survey = connect.fetchall() 

        groupCodeAnswers = dict(map(lambda k_v: (k_v[0], tuple(map(partial(GenerateAhpDewan.del_ret, key="code_answer"), k_v[1]))),groupby(survey, itemgetter("code_answer"))))
        groups = []
        for k, v in groupCodeAnswers.items():
            groups.append({"code_answer" : k, "value" : v})
        
        valueCodeAnswer = []
        for i in range(0, len(groups)):
            pointCitra = 0
            pointEksistensi = 0
            for j in range(0, len(groups[i]['value'])):
                if ((groups[i]['value'][j]['id_survey_question'] == 15) or (groups[i]['value'][j]['id_survey_question'] == 16) or (groups[i]['value'][j]['id_survey_question'] == 17) or (groups[i]['value'][j]['id_survey_question'] == 18) or (groups[i]['value'][j]['id_survey_question'] == 19)):
                    pointCitra  += int(groups[i]['value'][j]['answer'])
                else:
                    pointEksistensi += int(groups[i]['value'][j]['answer'])
            valueCodeAnswer.append({"user_id" : groups[i]['value'][0]['user_id'], "point_citra" : pointCitra * 4, "point_eksistensi" : pointEksistensi * 4})

        groupDewan = dict(map(lambda k_v: (k_v[0], tuple(map(partial(GenerateAhpDewan.del_ret, key="user_id"), k_v[1]))),groupby(valueCodeAnswer, itemgetter("user_id"))))
       
        arrayGroupDewan = []
        for k, v in groupDewan.items():
           arrayGroupDewan.append({"user_id" : k, "value" : v})
        
        result = []
        for i in range(0, len(arrayGroupDewan)):
            finalPointCitra = 0
            finalPointEksistensi = 0
            for j in range(0, len(arrayGroupDewan[i]['value'])):
                finalPointCitra += arrayGroupDewan[i]['value'][j]['point_citra']
                finalPointEksistensi += arrayGroupDewan[i]['value'][j]['point_eksistensi']
            result.append({"user_id" : arrayGroupDewan[i]['user_id'],"point_citra" : finalPointCitra / len(arrayGroupDewan[i]['value']) , "point_eksistensi" : finalPointEksistensi / len(arrayGroupDewan[i]['value']) })
        
        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in result:
            sql_update = "UPDATE tbl_ahp_dprd SET popularitas_eksistensi = %s, popularitas_citra = %s, updated_at = %s WHERE user_id = %s"
            value = (item['point_eksistensi'], item['point_citra'], updatedAt, item['user_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
        return "berhasil"
    
    def del_ret(d, key):
        del d[key]
        return d

