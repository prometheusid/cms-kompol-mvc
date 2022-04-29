from project import app
import nest_asyncio
# nest_asyncio.apply()
import twint

@app.route("/dashboard/crawling")
def cp_crawling():
    c = twint.Config()
    c.Search = 'fadli zon'
    c.Pandas = True
    c.Limit = 10
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    Tweets_df.head()

    # 1. angota punya dataset twntang diri dia
    # insert into sentiment_dprd
    # id, user_id, tweet
    return str(Tweets_df['tweet'])