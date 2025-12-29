from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Author, Publication

router = APIRouter(prefix="/queries")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. WHERE with multiple conditions
@router.get("/where")
def publications_after_year_in_journal(year: int, journal: str, db: Session = Depends(get_db)):
    return db.query(Publication).filter(
        Publication.year >= year,
        Publication.journal.ilike(f"%{journal}%")
    ).all()

# 2. JOIN
@router.get("/join")
def publications_with_authors(
    limit: int = Query(100, ge=1, le=100, description="Maximum number of rows to return (capped at 100)"),
    offset: int = Query(0, ge=0, description="Row offset for pagination"),
    db: Session = Depends(get_db)
):
    """Return publications joined with their authors.

    The `limit` parameter is restricted to a maximum of 100 rows to avoid very large joins.
    """
    result = db.query(Publication, Author).join(Author).limit(limit).offset(offset).all()
    return [
        {
            "title": p.title,
            "journal": p.journal,
            "year": p.year,
            "author": a.name
        }
        for p, a in result
    ]

# 3. GROUP BY
@router.get("/group_by_year")
def count_publications_by_year(db: Session = Depends(get_db)):
    rows = db.query(
        Publication.year,
        func.count(Publication.id).label("count")
    ).group_by(Publication.year).all()

    return [{"year": y, "count": c} for y, c in rows]

# 4. UPDATE with nontrivial condition
@router.put("/update_doi")
def update_doi_prefix(db: Session = Depends(get_db)):
    pubs = db.query(Publication).filter(
        Publication.doi.isnot(None),
        ~Publication.doi.startswith("https://doi.org/")
    ).all()

    for p in pubs:
        p.doi = "https://doi.org/" + p.doi

    db.commit()
    return {"updated": len(pubs)}

# 5. SORT by a field
@router.get("/sorted")
def publications_sorted_by_year(desc: bool = True, db: Session = Depends(get_db)):
    if desc:
        return db.query(Publication).order_by(Publication.year.desc()).all()
    else:
        return db.query(Publication).order_by(Publication.year.asc()).all()

@router.get("/stats/years")
def stats(db: Session = Depends(get_db)):
    return db.execute("""
        SELECT year, COUNT(*) FROM publications
        GROUP BY year ORDER BY year
    """).fetchall()