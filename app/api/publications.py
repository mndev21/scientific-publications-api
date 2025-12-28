from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Publication, Author

router = APIRouter(prefix="/publications")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_publication(pub: dict, db: Session = Depends(get_db)):
    author_name = pub.pop("author", None)

    author = None
    if author_name:
        author = db.query(Author).filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.add(author)
            db.commit()
            db.refresh(author)

    obj = Publication(**pub, author_id=author.id if author else None)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
