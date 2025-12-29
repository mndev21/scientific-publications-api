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
    # Preferred: incoming payload contains 'authors' list of dicts
    if "authors" in pub and pub["authors"]:
        a = pub["authors"][0]
        # prefer family name as stored name; if family missing, use combined given+family
        family = a.get("family", "") or ""
        full_name = family if family else f"{a.get('given','')} {a.get('family','')}".strip()

        author = db.query(Author).filter(
            Author.name == full_name
        ).first()

        if not author:
            author = Author(
                name=full_name,
                affiliation=str(a.get("affiliation", [])) if a.get("affiliation") else None
            )
            db.add(author)
            db.flush()
    # Fallback: loader or other clients may send a single 'author' string
    elif "author" in pub and pub.get("author"):
        name = pub.get("author")
        author = db.query(Author).filter(Author.name == name).first()
        if not author:
            author = Author(name=name)
            db.add(author)
            db.flush()

    pub_data = pub.copy()
    # remove possible extra keys not present on Publication
    pub_data.pop("authors", None)
    pub_data.pop("author", None)

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
