# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# Fast API
from fastapi import FastAPI, Body, Query

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get('/')
def home():
    return {'helo': 'world'}

# Request and response body
@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query parameters

@app.get('/person/detail')
def person_detail(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: int = Query(..., gt=0, lt=99)
):
    return {name: age}