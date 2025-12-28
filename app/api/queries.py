from fastapi import APIRouter, Depends
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
def publications_with_authors(db: Session = Depends(get_db)):
    return db.query(Publication, Author).join(Author, Publication.author_id == Author.id).all()

# 3. GROUP BY
@router.get("/group_by_year")
def count_publications_by_year(db: Session = Depends(get_db)):
    return db.query(Publication.year, func.count(Publication.id)).group_by(Publication.year).all()

# 4. UPDATE with nontrivial condition
@router.put("/update_doi")
def update_doi_prefix(prefix: str, db: Session = Depends(get_db)):
    publications = db.query(Publication).filter(Publication.doi.ilike("%10.%")).all()
    for pub in publications:
        pub.doi = prefix + pub.doi
    db.commit()
    return {"updated": len(publications)}

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
