from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

class TestCaseBase(BaseModel):
    input_data: str
    expected_output: str

class TestCaseCreate(TestCaseBase):
    solution_id: int

class TestCase(TestCaseBase):
    id: int
    created_at: datetime
    solution_id: int

    class Config:
        from_attributes = True

class SolutionBase(BaseModel):
    code: str
    language: str

class SolutionCreate(SolutionBase):
    problem_id: int

class Solution(SolutionBase):
    id: int
    created_at: datetime
    problem_id: int
    test_cases: List[TestCase] = []

    class Config:
        from_attributes = True

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str
    source_url: str

class ProblemCreate(ProblemBase):
    tags: List[str] = []

class Problem(ProblemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    solutions: List[Solution] = []

    class Config:
        from_attributes = True

class PracticeRecordBase(BaseModel):
    problem_id: int
    mastery_level: float
    last_practiced: datetime
    next_review_date: datetime

class PracticeRecordCreate(PracticeRecordBase):
    pass

class PracticeRecord(PracticeRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
