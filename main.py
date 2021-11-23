# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# Fast API
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

class Location(BaseModel):
    city: str
    state:str
    country: str

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