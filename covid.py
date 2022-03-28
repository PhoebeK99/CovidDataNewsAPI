from collections import Counter
import pickle
from string import punctuation
import newsapi
import spacy
from newsapi import NewsApiClient
import pandas as pd
# from wordcloud import WordCloud


def get_keywords_eng(content):
  result = []
  pos_tag = ["NOUN", "PROPN", "VERB"]

  for token in content:
    if(token.text in nlp_eng.Defaults.stop_words or token.is_punct):
      continue
    if(token.pos_ in pos_tag):
      result.append(token.text)
  
  return result


nlp_eng = spacy.load('en_core_web_lg')
newsapi = NewsApiClient(api_key = '946b1167ecf7403dbeb7d0d382f9133a')

articles = newsapi.get_everything(q = 'coronavirus', language = 'en', from_param = '2022-02-28', to = '2022-03-27', sort_by = 'relevancy', page_size = 100)

filename = 'articlesCOVID.pckl'
pickle.dump(articles, open(filename, 'wb'))

dados = []
for index, article in enumerate(articles):
  for x in articles['articles']:
    title = x['title']
    description = x['description']
    content = x['content']
    dates = x['publishedAt']
    dados.append({'title': title, 'date': dates, 'desc': description, 'content': content})

df = pd.DataFrame(dados)
df = df.dropna()
df.head()

results = []
for contents in df.content.values:
  content = nlp_eng(contents)
  results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])
df['keywords'] = results


filename = 'data.pckl'
pickle.dump(df['keywords'], open(filename, 'wb'))

filename = 'mostCommonWords.txt'
f = open(filename, 'w+')

for i, article in enumerate(df['title']):
  f.write(article + ":\n")
  for key in df['keywords'][i]:
    f.write(key + " ")
  f.write("\n\n")