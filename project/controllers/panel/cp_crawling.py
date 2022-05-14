from project import app
import nest_asyncio
from flask import url_for, send_from_directory
import pickle
# nest_asyncio.apply()
import twint

@app.route("/dashboard/crawling")
def cp_crawling():
    c = twint.Config()
    c.Search = 'fadli zon'
    c.Pandas = True
    c.Limit = 100
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    Tweets_df.head()

    # 1. angota punya dataset twntang diri dia
    # insert into sentiment_dprd
    # id, user_id, tweet, created_at, updated_at
    
    return str(Tweets_df['tweet'])

@app.route("/dashboard/predict")
def cp_predict():
    text = ['kata iwan fals anggota dewan jangan tidur kalau sidang soal rakyat']
 
    with open(f'{app.root_path}/static/model-nb/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(f'{app.root_path}/static/model-nb/tf_new.pkl', 'rb') as f:
        tf_new = pickle.load(f)

    textTf = tf_new.transform(text)
    prediction = model.predict(textTf)

    return str(prediction)