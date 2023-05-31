from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
async def nlp(file: Request):
  data =  await file.json()
  nlp_file = jsonable_encoder(nlpdocument(data["file"]))
  return JSONResponse(content=nlp_file)