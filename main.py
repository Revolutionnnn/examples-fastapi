# Python
from enum import Enum
from typing import Optional

# FastAPO
from fastapi import Body, Query, Path
from fastapi import FastAPI
from fastapi import status

# Pydantic
from pydantic import BaseModel, Field, IPvAnyAddress, HttpUrl, EmailStr

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
    password: str = Field(
        min_length=8,
    )

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
                "website_url": "https://www.live.com",
                "password": "@12asasdas12."
            }
        }


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )  # path operation decorator
def home():  # path operation function
    return {"hello": "World"}  # JSON


#  Request and Response body

@app.post(
            path="/person/new",
          response_model=Person,
          response_model_exclude={"password"},
          status_code=status.HTTP_201_CREATED
          )
def create_person(person: Person = Body()):
    return person


#  Validaciones: Querry parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK)
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title="Person name",
            description="This is the person name. It' s between 1 and 50 characters",
            example="Rocio"
        ),
        age: Optional[str] = Query(
            title="Person Age",
            description="This is the person age. It's required",
            example=25
        )
):
    return {name: age}


#  Validaciones: Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK)
def show_person(
        person_id: int = Path(
            gt=0,
            example=123
        )
):
    return {person_id: "it exists!"}


#  Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK)
def update_person(
        person_id: int = Path(
            title="Person ID",
            description="This is the person ID",
            gt=0,
            example=123
        ),
        person: Person = Body(),
        location: Location = Body()
):
    result = person.dict()
    result.update(location.dict())
    return result
