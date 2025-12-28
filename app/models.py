# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    publications = relationship("Publication", back_populates="author")


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    journal = Column(String)
    year = Column(Integer)
    doi = Column(String)
    abstract = Column(JSON)
    metadata_json = Column(JSONB)

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="publications")
