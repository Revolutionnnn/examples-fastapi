# Python
from enum import Enum
from typing import Optional

# FastAPO
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException

# Pydantic
from pydantic import BaseModel, Field, IPvAnyAddress, HttpUrl, EmailStr, SecretStr

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


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='gus')
    password: str = Field(..., min_length=2, max_length=20, example='123')
    message: str = Field(default='Login successful :)', description='Description message')


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
)  # path operation decorator
def home():  # path operation function
    return {"hello": "World"}  # JSON


#  Request and Response body

@app.post(
    path="/person/new",
    response_model=Person,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
)
def create_person(person: Person = Body()):
    return person


#  Validaciones: Querry parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
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

persons = [1, 2, 3, 4]


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"])
def show_person(
        person_id: int = Path(
            gt=0,
            example=123
        )
):
    if person_id not in persons:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="This person is not exist"
        )
    return {person_id: "it exists!"}


#  Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"])
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


@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=200,
    response_model_exclude={'password'},
    tags=["Login", "Persons"]
)
def login(username: str = Form(...), password: SecretStr = Form(...)):
    return LoginOut(username=username, password=password)


#  Cookies and headers parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contacts"]
)
def contact(
        first_name: str = Form(
            max_length=20,
            min_length=1
        ),
        last_name: str = Form(
            max_length=20,
            min_length=1
        ),
        email: EmailStr = Form(),
        message: str = Form(
            min_length=20
        ),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
):
    return user_agent


@app.post(
    path="/post-image",
    tags=["Image"]
)
def post_image(
        image: UploadFile = File()
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, 2)
    }
