from fastapi import FastAPI, Depends
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
