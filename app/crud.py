from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
import math
from . import models, schemas

def get_problem(db: Session, problem_id: int):
    return db.query(models.Problem)\
        .options(joinedload(models.Problem.solutions).joinedload(models.Solution.test_cases))\
        .filter(models.Problem.id == problem_id)\
        .first()

def get_problems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Problem)\
        .options(joinedload(models.Problem.solutions).joinedload(models.Solution.test_cases))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_or_create_tag(db: Session, tag_name: str):
    tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
    if not tag:
        tag = models.Tag(name=tag_name)
        db.add(tag)
        db.commit()
    return tag

def create_problem(db: Session, problem: schemas.ProblemCreate):
    db_problem = models.Problem(
        title=problem.title,
        description=problem.description,
        difficulty=problem.difficulty,
        source_url=problem.source_url
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    # Add tags
    for tag_name in problem.tags:
        tag = get_or_create_tag(db, tag_name)
        db_problem.tags.append(tag)
    
    db.commit()
    return db_problem

def create_solution(db: Session, solution: schemas.SolutionCreate):
    db_solution = models.Solution(
        problem_id=solution.problem_id,
        code=solution.code,
        language=solution.language
    )
    db.add(db_solution)
    db.commit()
    return db_solution

def get_solutions(db: Session, problem_id: int):
    return db.query(models.Solution)\
        .options(joinedload(models.Solution.test_cases))\
        .filter(models.Solution.problem_id == problem_id)\
        .all()

def create_test_case(db: Session, test_case: schemas.TestCaseCreate):
    db_test_case = models.TestCase(
        solution_id=test_case.solution_id,
        input_data=test_case.input_data,
        expected_output=test_case.expected_output
    )
    db.add(db_test_case)
    db.commit()
    return db_test_case

def get_practice_record(db: Session, problem_id: int):
    return db.query(models.PracticeRecord).filter(
        models.PracticeRecord.problem_id == problem_id
    ).first()

def calculate_next_review_date(mastery_level: float) -> datetime:
    """
    Calculate the next review date based on mastery level using a spaced repetition algorithm.
    The interval increases as mastery level increases.
    """
    base_interval = 1  # base interval in days
    multiplier = math.exp(mastery_level * 2)  # exponential increase with mastery
    days = base_interval * multiplier
    return datetime.now() + timedelta(days=days)

def update_practice_record(db: Session, problem_id: int, success: bool):
    record = get_practice_record(db, problem_id)
    
    if not record:
        record = models.PracticeRecord(
            problem_id=problem_id,
            mastery_level=0.0,
            last_practiced=datetime.now(),
            next_review_date=datetime.now()
        )
        db.add(record)
    
    # Update mastery level based on success
    if success:
        record.mastery_level = min(1.0, record.mastery_level + 0.1)
    else:
        record.mastery_level = max(0.0, record.mastery_level - 0.1)
    
    record.last_practiced = datetime.now()
    record.next_review_date = calculate_next_review_date(record.mastery_level)
    
    db.commit()
    return record

def get_problems_for_practice(db: Session, limit: int = 10):
    """
    Get problems that are due for practice based on next_review_date
    """
    return db.query(models.Problem)\
        .options(joinedload(models.Problem.solutions).joinedload(models.Solution.test_cases))\
        .join(models.PracticeRecord)\
        .filter(models.PracticeRecord.next_review_date <= datetime.now())\
        .order_by(models.PracticeRecord.next_review_date)\
        .limit(limit)\
        .all()
