from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True)
    title = Column(Text, index=True)
    year = Column(Integer)
    journal = Column(String)
    doi = Column(String, unique=True)
    abstract = Column(JSONB)
    metadata = Column(JSONB)

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author")
