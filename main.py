from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class School(BaseModel):
    school_name: str
    country:str
    student_count: int
    isAccepting: Optional[bool] = None

database = []

@app.get('/')
def index():
    return {'Hello':'This is my API'}

@app.get('/schools')
def get_schools():
    return database

@app.delete('/delete_school')
def delete_school(id:int):
    return database.remove(database[id])

@app.post('/add_schools')
def add_schools(school_id:int,school_name:str,country:str,student_count:str,isAccepting:bool):
    new_school = {
        "school_id":school_id,
        "school_name":school_name,
        "country":country,
        "student_count":student_count,
        "isAccepting":isAccepting
        }
    database.append(new_school)
    return new_school

