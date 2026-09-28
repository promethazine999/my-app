from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI(title="FastAPI", version="0.115.0")

class UserCreate(BaseModel):
    name: str
    email: str

class UserInfo(BaseModel):
    id: int
    name: str
    email: str

users_db = [
    {"id": 1, "name": "Ivan Ivanov", "email": "i.i.ivanov@mail.com"},
    {"id": 2, "name": "Petr Petrov", "email": "p.p.petrov@mail.com"},
]

@app.get("/api/v1/user", response_model=UserInfo)
def get_user(email: str):
    for u in users_db:
        if u["email"] == email:
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/v1/user", status_code=201)
def create_user(user: UserCreate):
    for u in users_db:
        if u["email"] == user.email:
            raise HTTPException(status_code=409, detail="User with this email already exists")
    new_id = max([u["id"] for u in users_db], default=0) + 1
    new_user = {"id": new_id, "name": user.name, "email": user.email}
    users_db.append(new_user)
    return new_id

@app.delete("/api/v1/user", status_code=204)
def delete_user(email: str):
    for i, u in enumerate(users_db):
        if u["email"] == email:
            users_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="User not found")
