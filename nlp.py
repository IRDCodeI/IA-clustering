from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import nltk
import math
import re


nltk.download('stopwords')

stw_eng = stopwords.words('english')
stemmer = PorterStemmer()

def nlpdocument(file):      
    df = pd.DataFrame(file["data"],index = None, columns = file["index"])

    file = df.copy(deep=True)
    file = file.apply(lambda x: x.apply(normalize))
    file = file.apply(lambda x: x.apply(doc_tokens, "broadcast"))

    # >> Bagwords
    tokens = element_df(file)
    doc = element_df(df)
    bagw = bag_words(columns = [doc], index = [tokens])
    tfidf = tf_idf(bagw)

    return tfidf
    

def normalize(doc):
  if not isinstance(doc, (float, int)):
    doc = re.sub("[^A-Za-z0-9?(')]", " ", doc).lower()
    doc = re.sub("(^[\s]*)|[()]|[?]", '', doc)
    doc = re.sub("\s{2,}",' ', doc)

  return doc

def tokenize_document(doc):
  doc_array = np.array(doc.split(" "), dtype=str)
  doc_array = doc_array[np.in1d(doc_array, stw_eng, invert=True)]
  doc_array = np.delete(doc_array, np.char.isdigit(doc_array))
  doc_array = np.unique(doc_array)

  return list(doc_array)

def doc_tokens(docs):

  tokens = []

  if not isinstance(docs, (float, int)):
 
    tokens = tokens + tokenize_document(docs)

    for i, token in enumerate(tokens):
      if token in stw_eng:
        tokens.remove(i)
      else:
        tokens[i] = stemmer.stem(token)

    tokens = np.unique(np.array(tokens, dtype=object).ravel())
    tokens = np.delete(tokens, np.where((tokens == "") | (tokens == "'")))

  return tokens
  

def element_df(df: pd.DataFrame, **kwargs):
    tokens = np.array([])
    for column in df.columns:
      list1 = df[column].values
      tokens = np.hstack((tokens, list1))
      tokens = np.hstack(tokens)
      tokens = np.unique(tokens)

    return tokens


# ---- UNTIL HERE ----

def bag_words(**kwarg):

  docs = []
  tokens = []

  for arg in kwarg.items():
    if arg[0] == 'columns':
      for list_column in arg[1]:        
        docs = docs + list(list_column)
    elif arg[0] == 'index':
      for list_index in arg[1]:
        tokens = tokens + list(list_index)

  bag_words_index = tokens
  bag_words_colums = list(range(0, len(docs)))

  bag_words = pd.DataFrame(columns= bag_words_colums, index= bag_words_index)
  
  #bag_words.apply(lambda x: pd.Series(docs).str.count(x.index).transpose(), axis =)

  for token in tokens:
    bag_words.loc[token] = pd.Series(docs).str.count(token).transpose()

  bagw_zeros = pd.Index(bag_words[bag_words.sum(axis = 1) == 0].index)
  bag_words = bag_words.drop(bagw_zeros, axis = 0)

  return bag_words

def tf_idf(bag_words: pd.DataFrame):
  df = []
  idf = []
  wtf = bag_words.copy()

  wtf = wtf.apply(lambda x: x.apply(tf_weigth))
  df = wtf.astype(bool).sum(axis=1)
  idf = pd.DataFrame(df.apply(idf_doc, size=bag_words.shape[1]))
  tf_idf = wtf*idf.values
  
  return tf_idf

  
def tf_weigth(value):
  if(value != 0):
    res = 1 + math.log10(value)
  else:
    res = 0
  
  return res

def idf_doc(value, size):
  if value != 0:
    res = math.log10(size/value)
  else:
    res = None

  return res
