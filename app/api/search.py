# app/api/search.py
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
def search_metadata(
    query: str = Query(..., description="Regex or text to search in metadata_json"),
    limit: int = Query(2, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Full-text search in metadata_json (JSONB) using pg_trgm + GIN index
    """
    results = db.query(Publication)\
                .filter(Publication.metadata_json.cast(String).op("~*")(query))\
                .offset(offset)\
                .limit(limit)\
                .all()
    
    return [
        {
            "id": pub.id,
            "title": pub.title,
            "metadata_json": pub.metadata_json
        }
        for pub in results
    ]
