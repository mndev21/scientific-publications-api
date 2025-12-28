# app/api/publications.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
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
    author = None

    if "authors" in pub and pub["authors"]:
        a = pub["authors"][0]

        author = db.query(Author).filter(
            Author.name == a.get("family", "")
        ).first()

        if not author:
            author = Author(
                name=a.get("family", ""),
                affiliation=str(a.get("affiliation", [])) if a.get("affiliation") else None
            )
            db.add(author)
            db.flush()

    pub_data = pub.copy()
    pub_data.pop("authors", None)

    obj = Publication(
        **pub_data,
        author_id=author.id if author else None
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ------------------------
# Pagination endpoint
# ------------------------
@router.get("/paginated")
def get_publications_paginated(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    items = db.query(Publication).order_by(Publication.id).limit(page_size).offset(offset).all()
    return {
        "page": page,
        "page_size": page_size,
        "items": items
    }


# ------------------------
# Search by regex over metadata_json
# ------------------------
@router.get("/search_metadata")
def search_metadata(q: str = Query(..., min_length=1), limit: int = 50, db: Session = Depends(get_db)):
    # Use raw SQL to leverage GIN + pg_trgm
    sql = text("""
        SELECT * FROM publications
        WHERE metadata_json::text ~ :pattern
        LIMIT :limit
    """)
    results = db.execute(sql, {"pattern": q, "limit": limit}).fetchall()
    return [dict(r) for r in results]
