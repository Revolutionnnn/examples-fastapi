# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPO
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()


#  Models

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


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