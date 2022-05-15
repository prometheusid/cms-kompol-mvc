""" from project import app
import nest_asyncio
# nest_asyncio.apply()
import twint

@app.route("/dashboard/crawling")
def cp_crawling():
    c = twint.Config()
    c.Search = 'dpr'
    c.Pandas = True
    c.Limit = 10
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    Tweets_df.head()
    return str(Tweets_df['tweet']) """