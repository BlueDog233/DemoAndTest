from fastapi import FastAPI, Body
from typing import Dict

from pydantic import BaseModel

from goods_interface.daichong_vip import common

app = FastAPI()
class DaichongDTO(BaseModel):
    tid: int
    inputvalue: str
    num: int

@app.post("/daichong_vip")  # use post, as we are sending data
async def daichong_vip(data:DaichongDTO):  # replace the comment with this
    result=common.buy(**data.dict())
    return {"code": 1, "message": result}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}