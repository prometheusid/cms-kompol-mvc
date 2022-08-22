from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
# Import Model
from project.models.LaporanKunjungan import LaporanKunjungan
from project.models.Info import Info
from project.models.Forum import Forum

from project.models.Profile import Profile

from project.models.Knn import Knn 

from project.models.Ahp import Ahp
from project.models.Calculate import Calculate
from project.models.Criteria import Criteria
from project.models.CalculateDewan import CalculateDewan
from project.models.Rekomendasi import Rekomendasi

#route index
@app.route('/', methods = ['GET'])
def pub_home():
    title = ("KOMUNIKASI POLITIK")
    laporan = LaporanKunjungan.fetchKunjungan3()
    forum = Forum.fetchDataForumHome()
    count = Forum.fetchCountForumHome()
    info = Info.fetchInfo3()

    # AHP PARTAI
    criteria = Ahp.fetchCriteriaPartai()
    value = Criteria.perbandingan([criteria['c12'], criteria['c13'], criteria['c14'], criteria['c23'], criteria['c24'], criteria['c34']], 4)
    dataAhpPartai = Ahp.fetchValue()
    sumDataAhpPartai = Ahp.sumValue()
    ahpPartai = Calculate.eigen_partai(dataAhpPartai, sumDataAhpPartai, value['rata_eigen'])
        
    # AHP DEWAN
    criteriaDewan = Ahp.fetchCriteriaDewan()
    valueDewan = Criteria.perbandingan([criteriaDewan['c12'], criteriaDewan['c13'], criteriaDewan['c14'], criteriaDewan['c15'], criteriaDewan['c23'], criteriaDewan['c24'], criteriaDewan['c25'], criteriaDewan['c34'], criteriaDewan['c35'], criteriaDewan['c45']], 5)
    dataAhpDewan = Ahp.fetchValueDewan()
    sumDataAhpDewan = Ahp.sumValueDewan()
    ahpDewan = CalculateDewan.eigen_dewan(dataAhpDewan, sumDataAhpDewan, valueDewan['rata_eigen'])
    

    # Rekomendasi partai
    sortScore = Rekomendasi.getHighestScoreAhpPartai(ahpPartai)
    dataRekomendasiPartai = Rekomendasi.getPartaiRekomendasi(sortScore)

    sortScoreDwn = Rekomendasi.getHighestScoreAhpDewan(ahpDewan)
    dataRekomendasiDewan = Rekomendasi.getDewanRekomendasi(sortScoreDwn)
    
    if 'loggedin' in session:
        sess = session['id']
        profiles = Profile.detaiilProfile(sess)

        dataPartai = Ahp.fetchValueId(sess)
        dataDewan = Ahp.fetchDewanId(sess)

        key = ''
        if session['role'] == 3:
            for row in ahpDewan:
                sentimentRek = row['value'][2]
                popularitasRek = row['value'][1]
                akuntabilitasRek = row['value'][3]
                integritasRek = row['value'][4]

                if row['user_id'] == dataDewan['user_id']:
                    if popularitasRek < sentimentRek and popularitasRek < integritasRek:
                        key = 'Menaikan Popularitas'
                    if akuntabilitasRek <integritasRek and akuntabilitasRek < sentimentRek:
                        key = 'Memperbaiki akuntabilitas'
                    if integritasRek < sentimentRek and integritasRek < popularitasRek:
                        key ='Menjaga Integritas'
                    if sentimentRek < popularitasRek and sentimentRek < akuntabilitasRek:
                        key = 'Menaikan Kinerja'
                        
        rekomendasi = Knn.knn(key)
        return render_template('public/homepage/index.html', title=title, profiles=profiles, laporan=laporan, info=info, forum=forum, count = count, rekomendasi = rekomendasi, ahpPartai=ahpPartai, dataPartai=dataPartai, ahpDewan=ahpDewan, dataDewan=dataDewan, rekomendasiPartai = dataRekomendasiPartai, rekomendasiDewan = dataRekomendasiDewan)
    return render_template('public/homepage/index.html', title=title, laporan=laporan, info=info, forum=forum, count = count, rekomendasiPartai = dataRekomendasiPartai, rekomendasiDewan = dataRekomendasiDewan)

@app.route("/rekomendasi", methods=["GET", "POST"])
def pub_rekomendas():
    data = 'Sentiment Masyarakat'
    rekomendasi = Knn.knn(data)
    return rekomendasi
