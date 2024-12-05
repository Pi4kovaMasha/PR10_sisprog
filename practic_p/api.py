from fastapi import FastAPI, HTTPException
import uvicorn
from models import *
from config import *
from response_models import *
from fastapi import Query

from pydantic import BaseModel

class UserUpdate(BaseModel):
    user_name: str
    user_role: str

app = FastAPI(
    title="yourtitle",
    description="pracAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/users/select/{user_id}")
async def get_users(user_id:int):
    try:
        with DBSettings.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            return user
    except:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/add", response_model=UserCreate)
async def add_users(user_name:str, user_role:str):
    user = UserCreate(name=user_name, role = user_role)
    with DBSettings.get_session() as conn:
        roleDB = conn.query(Role).filter(Role.name == user.role).first()
        if (roleDB == None):
            raise HTTPException(status_code=404, detail="We have not this role")
        else:
            new_user = User(name = user.name, role_id = roleDB.id)
            conn.add(new_user)
            conn.commit()
            print("Успешно")
            return(user)

@app.put("/users/update/{user_id}", response_model=UserRead)
async def update_users(user_id: int, user_name: str = None, user_role: str = None):
    with DBSettings.get_session() as conn:
        user = conn.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user_name:
            user.name = user_name
        if user_role:
            roleBD = conn.query(Role).filter(Role.name == user_role).first()
            if not roleBD:
                raise HTTPException(status_code=404, detail="We don't have this role")
            user.role_id = roleBD.id
        
        conn.commit()
        return UserRead(id=user.id, name=user.name, role=user_role)



@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int):
    with DBSettings.get_session() as conn:
        user = conn.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        conn.delete(user)
        conn.commit()
        print("User deleted successfully")
        return {"detail": "User deleted successfully"}

uvicorn.run(app, host="127.0.0.1", port=8000)