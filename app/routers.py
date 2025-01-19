from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database, models
from .file_manager import FileManager

router = APIRouter()
file_manager = FileManager("solutions")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/problems/", response_model=schemas.Problem)
def create_problem(problem: schemas.ProblemCreate, db: Session = Depends(get_db)):
    return crud.create_problem(db=db, problem=problem)

@router.get("/problems/", response_model=List[schemas.Problem])
def read_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    problems = crud.get_problems(db, skip=skip, limit=limit)
    return problems

@router.get("/problems/{problem_id}", response_model=schemas.Problem)
def read_problem(problem_id: int, db: Session = Depends(get_db)):
    db_problem = crud.get_problem(db, problem_id=problem_id)
    if db_problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem

@router.post("/solutions/", response_model=schemas.Solution)
def create_solution(solution: schemas.SolutionCreate, db: Session = Depends(get_db)):
    return crud.create_solution(db=db, solution=solution)

@router.get("/problems/{problem_id}/solutions/", response_model=List[schemas.Solution])
def read_solutions(problem_id: int, db: Session = Depends(get_db)):
    solutions = crud.get_solutions(db, problem_id=problem_id)
    return solutions

@router.post("/test-cases/", response_model=schemas.TestCase)
def create_test_case(test_case: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    return crud.create_test_case(db=db, test_case=test_case)

@router.get("/practice/", response_model=List[schemas.Problem])
def get_practice_problems(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_problems_for_practice(db, limit=limit)

@router.post("/practice/{problem_id}/complete")
def complete_practice(problem_id: int, success: bool, db: Session = Depends(get_db)):
    return crud.update_practice_record(db, problem_id=problem_id, success=success)

@router.get("/solutions/{solution_id}/file")
def get_solution_file(solution_id: int, db: Session = Depends(get_db)):
    # Get solution from database
    solution = db.query(models.Solution).filter(models.Solution.id == solution_id).first()
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    # Load file content
    content = file_manager.load_solution(solution_id, solution.language)
    if content is None:
        raise HTTPException(status_code=404, detail="Solution file not found")
    
    return {"content": content, "language": solution.language}
