from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI(title="MySQL Users API")

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
