from pygooglenews import GoogleNews
from textblob import TextBlob
import pandas as pd
import numpy as np

# takes in the news language, news country, and the keyword to search for
# returns a list of news article entries with the title, link and publication date
def get_news(language:str, country_code:str, keyword:str):
    news_lst = []
    news = GoogleNews(lang=language, country=country_code)
    search = news.search(keyword)
    for i in search['entries']:
        news_lst.append({'title': i.title, 'link': i.link, 'date': i.published})
    return news_lst

# takes in the text to translate, the original language, and the target translation language
# returns the translation as a string
def translate(text:str, from_language:str, to_language:str):
    b = TextBlob(text)
    translation = str(b.translate(from_lang=from_language, to=to_language))
    return translation

# takes in the text on which the sentiment analysis will be conducted
# returns the sentiment measure
def get_sentiment(text:str):
    b = TextBlob(text)
    sentiment = b.sentiment.polarity
    return sentiment

# one of the topics I had to analyze during my summer internship at a hedge fund was China's property market
# I scrpaed Chinese news articles and serached for the keyword "real estate" (in Chinese)
data = pd.DataFrame(get_news("zh", "CN", "房地产"))

# create two new columns in the data frame to hold the translation and the sentiment analysis result
data["translation"] = data["title"].apply(translate, from_language="zh", to_language="en")
data["sentiment"] = data["translation"].apply(get_sentiment)

# create a new field to categorize the sentiment
data["sentiment-type"] = np.where(data["sentiment"]<0, "negative", np.where(data["sentiment"]>0, "positive", "neutral"))

# export results to Excel
data.to_excel("output.xlsx")











