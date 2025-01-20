from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates_16_5")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request":request, "users": users})



@ app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")




@app.post("/user/{username}/{age}", response_model=User)
async def create_user(username: str, age: int):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": f"User {user_id} has been deleted."}
    raise HTTPException(status_code=404, detail="User was not found")
