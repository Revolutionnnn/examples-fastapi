# Python
from typing import Optional, Dict, Any
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, IPvAnyAddress, HttpUrl, EmailStr

# FastAPO
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()


#  Models

class HairColor(str, Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        min_length=0,
        max_length=20
    )
    state: str = Field(
        min_length=0,
        max_length=20
    )
    country: str = Field(
        min_length=0,
        max_length=20
    )

    class Config:
        schema_extra = {
            "example": {
                "city": "Buenos aires",
                "state": "Provincia",
                "country": "Argentina"
            }
        }


class Person(BaseModel):
    first_name: str = Field(
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        min_length=1,
        max_length=50
    )
    age: int = Field(
        gt=0,
        le=150
    )
    hair_color: Optional[HairColor] = None
    is_married: Optional[bool] = Field(default=None)

    email: EmailStr = Field()
    addressIp: Optional[IPvAnyAddress] = Field()
    website_url: Optional[HttpUrl] = Field()

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Rodrigo",
                "last_name": "Lopez",
                "age": 30,
                "hair_color": "black",
                "is_married": False,
                "email": "maicol@gmail.com",
                "addressIp": "127.0.0.1",
                "website_url": "https://www.live.com"
            }
        }


@app.get("/")  # path operation decorator
def home():  # path operation function
    return {"hello": "World"}  # JSON


#  Request and Response body

@app.post("/person/new")
def create_person(person: Person = Body()):
    return person


#  Validaciones: Querry parameters

@app.get("/person/detail")
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title="Person name",
            description="This is the person name. It' s between 1 and 50 characters"
        ),
        age: Optional[str] = Query(
            title="Person Age",
            description="This is the person age. It's required"
        )
):
    return {name: age}


#  Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(gt=0)
):
    return {person_id: "it exists!"}


#  Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            title="Person ID",
            description="This is the person ID",
            gt=0
        ),
        person: Person = Body(),
        location: Location = Body()
):
    result = person.dict()
    result.update(location.dict())
    return result
