from typing import Optional
from pydantic import BaseModel, Field
import uuid


class UserModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username:str
    email:Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    

    class Config:
        allow_population_by_field_name = True

        schema_extra = {

            "example": {

                "username": "ilterkose",
                "email": "test@fastapi.com"

            }

        }
