from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session
from flask_mysqldb import MySQLdb
import csv

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process, fuzz

# generate random integer values
from random import seed
from random import randint

class Knn:
    data = pd.read_csv(f'{app.root_path}/static/dataset/rekomendasi/dataset-baru.csv',encoding="ISO-8859-1")
    result_df = data
    pivot_table = result_df.pivot(index='id',columns='recommendation_type',values='popularity').fillna(0)

    matrix_table = csr_matrix(pivot_table.values)
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors = 5)
    model_knn.fit(matrix_table)

    def rekomendasi(result,data,model,n_recommendation):
        model.fit(data)
        idx=process.extractOne(result,Knn.result_df['result'])[2]
        print('Data teratas',Knn.result_df['result'][idx],'\n')
        rekom = Knn.result_df['result'][idx]
        print('Data Lain untuk anda \n')
        distances, indices = model.kneighbors(data[idx], n_neighbors=n_recommendation)
        for i in indices:
            Rekomendasi = Knn.result_df['result'][i].where(i!=idx),distances
            
        return rekom

    def knn(post):
        hasil = Knn.rekomendasi(str(post),Knn.matrix_table,Knn.model_knn,5)
        return hasil