from fastapi import APIRouter,Depends, FastAPI,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from .model import UserModel

fake_users_test = {
    "ilter": {
        "username": "ilter",
        "full_name": "ilterkose",
        "email": "ilter@test.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "ceylin": {
        "username": "ceylin",
        "full_name": "ceylin",
        "email": "ceylin@test.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    return User(username = token + "fake",email="ilter@test.com")

def fake_has_password(password:str):
    return "fakehashed" + password



class UserInDB(UserModel):
    hashed_password:str
    

def get_user(db,username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    return get_user(fake_users_test,token)

async def get_current_user(token:str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},)
    
    return user
    
async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@router.post("/token")
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_test.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_has_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/me")
async def get_user_me(current_user:UserModel = Depends(get_current_user)):
    return current_user

