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
    author_data = pub.pop("author", None)

    author_obj = None
    if author_data and "name" in author_data:
        author_obj = db.query(Author).filter(
            Author.name == author_data["name"]
        ).first()

        if not author_obj:
            author_obj = Author(name=author_data["name"])
            db.add(author_obj)
            db.commit()
            db.refresh(author_obj)

    publication = Publication(**pub)

    if author_obj:
        publication.author_id = author_obj.id

    db.add(publication)
    db.commit()
    db.refresh(publication)

    return publication

@router.get("/")
def list_publications(db: Session = Depends(get_db)):
    return db.query(Publication).all()
