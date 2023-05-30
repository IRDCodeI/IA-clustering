from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing_extensions import Annotated
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
async def nlp(file: Request):
  data =  await file.json()
  nlpdocument(data["file"])
  return {
     "file_size": len(file)
  }