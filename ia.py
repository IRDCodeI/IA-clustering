from database import connection as db
from dotenv import load_dotenv
from bardapi import Bard
import openai
import requests
import pandas as pd
import nlp
import os
load_dotenv()

token = ''
key = ''
openai.api_key = key

cursor = db.cursor()

def requestModel(doc, **kwargs):

    for arg in kwargs.items():
        if arg[0] == "model" and arg[1] == "chatgpt":
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=[
                    {"role": "system", "content": "You are a helpful writer that can write long abstracts"},
                    {"role": "system", "content": f"You will create a long abstract with a length of tokens based on tokens key and the topic of the abstract based on the title key {doc}"},        
                ],
                temperature=0.7
            )

            return res.choices[0]["message"]["content"]
        elif arg[0] == "model" and arg[1] == "bard":
            session = requests.Session()
            session.headers = {
                "Host": "bard.google.com",
                "X-Same-Domain": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Origin": "https://bard.google.com",
                "Referer": "https://bard.google.com/",
            }
            session.cookies.set("__Secure-1PSID", token)

            bard = Bard(token= token, session= session, timeout= 30)
            bard.get_answer("You are a helpful writer that can write long abstracts")
            res = bard.get_answer(f"You will create a long abstract with a length of tokens based on tokens key and the topic of the abstract based on the title key {doc}")

            return(res["content"])



def generateAbstract(doc, **kwargs):

    abstract = ()
    tokens = []
    tokens_original = []
    sql = f"SELECT * FROM ai_abstract WHERE title = \"%s\" AND model = \"%s\";" % (doc['title'], doc['model'])
    res = cursor.execute(sql)

    if(res != 0):
        abstract = cursor.fetchone()
        abstract = abstract[3]
        tokens = countTokensAbstract(abstract)
        tokens_original = countTokensAbstract(doc['abstract'])
    else:
        for arg in kwargs.items():
            if (arg[0] == "model" and arg[1] == "chatgpt"):
                abstract = requestModel(doc, model = arg[1])
                sql = f"""INSERT INTO ai_abstract(title, abstract_original, abstract_generate, model) 
                        VALUES (\"{doc['title']}\", \"{doc['abstract']}\", \"{abstract}\", \"{doc['model']}\");"""
                
                tokens = countTokensAbstract(abstract)
                tokens_original = countTokensAbstract(doc['abstract'])
                 
                cursor.execute(sql)
            elif (arg[0] == "model" and arg[1] == "bard"):
                abstract = requestModel(doc, model = arg[1])
                sql = f"""INSERT INTO ai_abstract(title, abstract_original, abstract_generate, model) 
                        VALUES (\'{doc['title']}\', \'{doc['abstract']}\', \'{abstract}\', \'{doc['model']}\');"""

                countTokensAbstract(abstract)
                tokens = countTokensAbstract(abstract)
                tokens_original = countTokensAbstract(doc['abstract'])

                cursor.execute(sql)
            else:
                print("No selected model")
    
    return {"abstract": abstract, "tokens_generate": tokens, "tokens_original": tokens_original}

def countTokensAbstract(doc):

    doc = nlp.normalize(doc)
    tokens = nlp.doc_tokens(doc)

    return len(tokens)
