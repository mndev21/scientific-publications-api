from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Publication

router = APIRouter(prefix="/publications")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_publication(pub: dict, db: Session = Depends(get_db)):
    obj = Publication(**pub)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/")
def list_publications(db: Session = Depends(get_db)):
    return db.query(Publication).all()
