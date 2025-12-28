from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import String
from app.database import SessionLocal
from app.models import Publication

router = APIRouter(prefix="/queries")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search_metadata")
def search_metadata(query: str = Query(..., description="Regex or text to search in metadata_json"), 
                    db: Session = Depends(get_db)):
    """
    Full-text search in metadata_json (JSONB) using pg_trgm + GIN index
    """
    # Cast JSONB to text and use PostgreSQL regex match (~*) for case-insensitive search
    results = db.query(Publication).filter(
        Publication.metadata_json.cast(String).op("~*")(query)
    ).all()
    
    return [
        {
            "id": pub.id,
            "title": pub.title,
            "metadata_json": pub.metadata_json
        }
        for pub in results
    ]
