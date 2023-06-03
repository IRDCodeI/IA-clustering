from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ia import generateAbstract
from mds import mds
from metafile import meta
import typing

class Data(BaseModel):
    data: typing.Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/nlp/")
async def nlp(file: Request):
    data = await file.json()
    nlp_file = jsonable_encoder(mds(data["file"]))
    return JSONResponse(content=nlp_file)

@app.post("/meta/")
async def data(file: Request):
    data = await file.json()
    metafile = jsonable_encoder(meta(data["file"]))
    return JSONResponse(content=metafile)

@app.post("/ai_abstract/")
async def abstractGenerate(doc: Request):
    doc = await doc.json()    
    abstract = jsonable_encoder(generateAbstract(doc["doc"], model = doc["doc"]["model"]))
    return JSONResponse(content=abstract)
