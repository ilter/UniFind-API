from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uuid


class SchoolModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    school_name: str
    country: str
    student_count: int
    isAccepting: Optional[bool] = None

    class Config:
        allow_population_by_field_name = True

        schema_extra = {

            "example": {

                "school_name": "Ozyegin University",
                "country": "Turkey",
                "student_count": 1000,
                "isAccepting ": True,

            }

        }


class UpdateSchoolModel(BaseModel):
    student_count: int
    isAccepting: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "student_count": "5555",
                "isAccepting": True,
            }
        }
