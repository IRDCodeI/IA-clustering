import pandas as pd
import numpy as np
import re
import math

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')

stw_eng = stopwords.words('english')
stemmer = PorterStemmer()

def nlpdocument(file):      
    df = pd.DataFrame(file["data"],index = None, columns = file["index"])

    file = df.copy(deep=True)
    file = file.apply(lambda x: x.apply(normalize))
    file = file.apply(lambda x: x.apply(doc_tokens, "broadcast"))

    tokenize(file)
    

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

def tokenize(df: pd.DataFrame):
  list_df = []
  # Iterate through the columns of dataframe
  for column in df.columns:
    list1 = df[column].to_numpy().tolist()
    list_df.append(list1)
  
  print(list_df)
  


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
  
  for token in tokens:
    bag_words.loc[token] = list(np.char.count(docs, token))

  return bag_words

def tf_idf(bag_words: pd.DataFrame):
  df = []
  idf = []
  wtf = bag_words.copy()

  for doc in bag_words:
    wtf[doc] = wtf[doc].apply(tf_weigth)

  df = wtf.astype(bool).sum(axis=1)

  for value in df:
    idf.append(idf_doc(value))

  idf = pd.DataFrame(idf)
  tf_idf = wtf*idf.values

  return tf_idf

  
def tf_weigth(value):
  if(value != 0):
    res = 1 + math.log10(value)
  else:
    res = 0
  
  return res

def idf_doc(value):
  if value != 0:
    res = math.log10(bag_words.shape[1]/value)
  else:
    res = None

  return res
