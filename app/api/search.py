from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.models import Publication

router = APIRouter(prefix="/search")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Полнотекстовый поиск по JSON (abstract)
@router.get("/")
def search_abstract(regex: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT * FROM publications
        WHERE abstract::text ~ :regex
    """)
    result = db.execute(query, {"regex": regex}).fetchall()
    return [dict(r) for r in result]
