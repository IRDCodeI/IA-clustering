import openai
import os
from database import connection
from dotenv import load_dotenv
load_dotenv()

key = os.environ.get("ChatGPT_KEY")
openai.api_key = key

def requestModel(doc):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful writer that can write long abstracts"},
            {"role": "system", "content": f"You will create a long abstract with a length of tokens based on tokens key and the topic of the abstract based on the title key {doc}"},        
        ],
        temperature=0.7
    )

    return res.choices[0].content

def generateAbstract(doc, **kwargs):

    abstract = {}

    for item in kwargs.items():
        if (item == "ChatGPT"):
            abstract = requestModel(doc)
        else:
            print("No selected model")
    
    return abstract