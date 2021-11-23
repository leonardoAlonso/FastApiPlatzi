# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr

# Fast API
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red" 


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        lt=99
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(..., example="test@test.com")

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Leonardo",
                "last_name": "Alonso",
                "age": 26,
                "hair_color": "brown",
                "is_married": False
            }
        }

class Location(BaseModel):
    city: str = Field(..., min_length=1)
    state:str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)

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
    name: Optional[str] = Query(
        None,
            min_length=1,
            max_length=50,
            title="Person Name",
            description="This is the person name, It's between 1 and 50 characters"
        ),
    age: int = Query(
            ...,
            gt=0,
            lt=99,
            title="Person Age",
            description="This is the person age, It's bettween 0 and 99"
        )
):
    return {name: age}

# Validaciones: Path parameters

@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
            ...,
            gt=0,
            name="Person id",
            description="This is the id stored in the database, It should be grater than 0"
        )
):
    return {person_id: "It exists!"}

# Validaciones: Request body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title="Person id",
        description="This is the person id",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results