from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp import nlpdocument
import typing


class Data(BaseModel):
    data: typing.Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post('/nlp/')
async def nlp(data: Data):
  nlpdocument(data)
  return {"csv": "Data CSV"}