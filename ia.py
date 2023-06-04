from database import connection as db
from dotenv import load_dotenv
import openai
import os
load_dotenv()

key = "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"
openai.api_key = key
cursor = db.cursor()

def requestModel(doc):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful writer that can write long abstracts"},
            {"role": "system", "content": f"You will create a long abstract with a length of tokens based on tokens key and the topic of the abstract based on the title key {doc}"},        
        ],
        temperature=0.7
    )

    return res.choices[0]["message"]["content"]

def generateAbstract(doc, **kwargs):

    abstract = ()
    sql = f"SELECT * FROM ai_abstract WHERE title = \"%s\" AND model = \"%s\";" % (doc['title'], doc['model'])
    res = cursor.execute(sql)

    print(res)

    if(res != 0):
        abstract = cursor.fetchone()
        abstract = abstract[3]
    else:
        for arg in kwargs.items():
            if (arg[0] == "model" and arg[1] == "chatgpt"):
                abstract = requestModel(doc)
                sql = f"""INSERT INTO ai_abstract(title, abstract_original, abstract_generate, model) 
                        VALUES (\"{doc['title']}\", \"{doc['abstract']}\", \"{abstract}\", \"{doc['model']}\");"""

                print(sql)                    
                cursor.execute(sql)
            else:
                print("No selected model")
    
    return abstract