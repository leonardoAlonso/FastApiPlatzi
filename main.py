# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr

# Fast API
from fastapi import FastAPI, Body, Query, Path, Form, Header, Cookie
from fastapi import status

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class BasePerson(BaseModel):
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
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Leonardo",
                "last_name": "Alonso",
                "age": 26,
                "hair_color": "brown",
                "is_married": False,
                "email": "",
                "password": ""
            }
        }


class Person(BasePerson):
    password: str = Field(..., min_length=8)


class PersonOut(BasePerson):
    pass


class Location(BaseModel):
    city: str = Field(..., min_length=1)
    state:str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)


class LoginOut(BaseModel):
    username:str = Field(..., max_length=20, example="Leo")
    message:str = Field(default="Login succesfully")


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
def home():
    return {'helo': 'world'}

# Request and response body
@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK
)
def person_detail(
    name: Optional[str] = Query(
        None,
            min_length=1,
            max_length=50,
            title="Person Name",
            description="This is the person name, It's between 1 and 50 characters",
            example="Leonardo"
        ),
    age: int = Query(
            ...,
            gt=0,
            lt=99,
            title="Person Age",
            description="This is the person age, It's bettween 0 and 99",
            example=26
        )
):
    return {name: age}

# Validaciones: Path parameters

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK
)
def show_person(
    person_id: int = Path(
            ...,
            gt=0,
            name="Person id",
            description="This is the id stored in the database, It should be grater than 0",
            example=4
        )
):
    return {person_id: "It exists!"}

# Validaciones: Request body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK
)
def update_person(
    person_id: int = Path(
        ...,
        title="Person id",
        description="This is the person id",
        gt=0,
        example=5
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

# Formularios

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password:str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_nameL:str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent
