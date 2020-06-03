#https://medium.com/daily-python/python-script-to-search-for-news-based-on-keywords-daily-python-5-509348bd190e
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='this should be newsapi key')
news_sources = newsapi.get_sources()
for source in news_sources['sources']:
    print(source['name'])

top_headlines = newsapi.get_top_headlines(
    q='Covid-19',
    language='en',
)
for article in top_headlines['articles']:
    print('Title : ',article['title'])
    print('Description : ',article['description'],'\n\n')

all_articles = newsapi.get_everything(
    q='Covid-19',
    language='en',
)

replyList=[]
for article in all_articles['articles']:
    mydict1 = {"Source": "ss", "Title": "name", "Description": '234'}
    mydict1["Source"] = article['source']['name']
    mydict1["Title"] = article['title']
    mydict1["Description"] = article['description']

    mydict1["Source"] = article['source']['name']
    replyList.append(mydict1)
    print('Source : ', article['source']['name'])
    print('Title : ',article['title'])
    print('Description : ',article['description'],'\n')


