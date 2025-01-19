from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

# Many-to-many relationship tables
problem_tags = Table(
    'problem_tags',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    difficulty = Column(String)
    source_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    solutions = relationship("Solution", back_populates="problem")
    tags = relationship("Tag", secondary=problem_tags, back_populates="problems")
    practice_records = relationship("PracticeRecord", back_populates="problem")

class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    code = Column(String)
    language = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    problem = relationship("Problem", back_populates="solutions")
    test_cases = relationship("TestCase", back_populates="solution")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("solutions.id"))
    input_data = Column(String)
    expected_output = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    solution = relationship("Solution", back_populates="test_cases")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationships
    problems = relationship("Problem", secondary=problem_tags, back_populates="tags")

class PracticeRecord(Base):
    __tablename__ = "practice_records"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    mastery_level = Column(Float, default=0.0)  # 0.0 to 1.0
    last_practiced = Column(DateTime(timezone=True))
    next_review_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    problem = relationship("Problem", back_populates="practice_records")
