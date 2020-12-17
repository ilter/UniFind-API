from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import Database
from .models import SchoolModel, UpdateSchoolModel

router = APIRouter()

database = Database().get_database()


@router.get('/')
def index():
    return {'Hello': 'Welcome the Schools API'}


@router.get("/all", response_description="Get All Schools")
async def all_schools():
    schools = []
    for school in database.find():
        schools.append(school_help(school))
    return schools


@router.post("/add", response_description="Add new School")
async def add_school(school: SchoolModel = Body(...)):
    school = jsonable_encoder(school)
    new_school = database.insert_one(school)

    check_school = database.find_one(
        {"_id": new_school.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=check_school)


@router.get("/{id}", response_description="Get single School")
async def show_school(id: str):
    school = database.find_one({"_id": id})
    if school is not None:
        return school
    raise HTTPException(status_code=404, detail="School with {} is none".format(id))


@router.delete("/{id}", response_description="Delete School")
async def delete_school(id: str):
    delete_result = database.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return True

    raise HTTPException(status_code=404, detail=f"School is not found")


@router.put("/{id}", response_description="Update School")
async def update_school(id: str, school: UpdateSchoolModel = Body(...)):
    school = {x: y for x, y in school.dict().items() if y is not None}
    update_result = database.update_one({"_id": id}, {"$set": school})

    if update_result.modified_count == 1:
        updated_school = database.find_one({"_id": id})
        if updated_school is not None:
            return updated_school

    existing_school = database.find_one({"_id": id})
    if existing_school is not None:
        return existing_school

    raise HTTPException(status_code=404, detail=f"School {id} not found")


# Helper Functions
def school_help(school) -> dict:
    return {
        "id": str(school["_id"]),
        "school_name": school["school_name"],
        "country": school["country"],
        "student_count": school["student_count"],
        "isAccepting": school["isAccepting"],
    }
