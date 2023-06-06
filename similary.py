import pandas as pd
import numpy as np
import math
import uuid
from database import connection
from nlp import nlpdocument
from sklearn.metrics.pairwise import pairwise_distances

def getSimilarityDocs(doc):
    cursor = connection.cursor()
    sql = f"SELECT * FROM ai_abstract WHERE model = '{doc['model']}';"
    res = cursor.execute(sql)

    if(res != 0):
        dataset = cursor.fetchall()
        dataset = pd.DataFrame(dataset, columns=["id","title","abstract", "abstract_generate", "model"]) 
        index = dataset[dataset.title == doc["title"]].index.to_list()[0]  

        bagw = nlpdocument(dataset[["abstract", "abstract_generate"]]).transpose()
        docs = dataset.shape[0]

        cosine_docs = distance_doc(bagw)
        jacard_docs = jacard_doc(wtf(bagw))

        jacard = jacard_docs.iloc[0:docs,docs:]
        jacard = jacard.iloc[index, index]

        cosine = cosine_docs.iloc[0:docs,docs:]
        cosine = cosine.iloc[index, index]

        mean_cosine = cosine_docs.iloc[0:docs,docs:].mean().sum()/docs
        mean_jacard = jacard_docs.iloc[0:docs,docs:].mean().sum()/docs

    response = {"jacard":jacard, "mean_jacard":mean_jacard, "cosine": cosine, "cosine_mean":mean_cosine}

    return response

def getDocumentsBD(model):
  response = []
  cursor = connection.cursor()
  sql = f"SELECT title FROM ai_abstract WHERE model = '{model}';"

  res = cursor.execute(sql)

  if(res != 0):
    titles = cursor.fetchall()

    for title in titles:
      response.append({"name": title[0], "code": uuid.uuid4()})

  return response         

def distance_doc(tf_idf: pd.DataFrame):
  distance = []

  module = tf_idf.pow(2, axis = 0)
  module = pd.Series(module.sum(axis = 0).apply(np.sqrt))
  
  norm_vect = tf_idf.div(module, level = 1, axis=1)

  for column in norm_vect:
    distance.append(norm_vect.apply(lambda x: norm_vect[column].mul(x, axis="index").sum(axis=0), axis = 0))

  distance =  1.00 - pd.DataFrame(distance)

  return distance.round(4).abs()


def jacard_doc(bag_words: pd.DataFrame):
  jacard = []

  bag_words = bag_words.apply(lambda x: x.astype(bool))
  
  jacard = pd.DataFrame(
      1 - pairwise_distances(bag_words.T.to_numpy(), metric='jaccard'), 
      index=bag_words.columns, columns=bag_words.columns,
  )

  return 1-jacard.round(4).abs()

def wtf(bag_words: pd.DataFrame):
  df = []
  idf = []
  wtf = bag_words.copy()

  wtf = wtf.apply(lambda x: x.apply(tf_weigth))

  return wtf

def tf_weigth(value):
  if(value != 0):
    res = 1 + math.log10(value)
  else:
    res = 0
  
  return res