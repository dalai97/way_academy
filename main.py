from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI(title="MySQL Users API")

class UserCreate(BaseModel):
    name: str

class UserUpdate(BaseModel):
    name: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id, name FROM users ORDER BY id DESC")).mappings().all()
    return rows

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT id, name FROM users WHERE id = :user_id"),
        {"user_id": user_id},
    ).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return row

@app.post("/users", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    result = db.execute(
        text("INSERT INTO users (name) VALUES (:name)"),
        {"name": payload.name},
    )
    db.commit()
    user_id = result.lastrowid
    row = db.execute(
        text("SELECT id, name FROM users WHERE id = :user_id"),
        {"user_id": user_id},
    ).mappings().first()
    return row

@app.put("/users/{user_id}")
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    result = db.execute(
        text("UPDATE users SET name = :name WHERE id = :user_id"),
        {"name": payload.name, "user_id": user_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    row = db.execute(
        text("SELECT id, name FROM users WHERE id = :user_id"),
        {"user_id": user_id},
    ).mappings().first()
    return row

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM users WHERE id = :user_id"),
        {"user_id": user_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None
