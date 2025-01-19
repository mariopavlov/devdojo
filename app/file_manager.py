import os
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas

class FileManager:
    def __init__(self, base_path: str = "solutions"):
        """Initialize the FileManager with a base path for storing solution files."""
        self.base_path = Path(base_path)
        # Create the base directory if it doesn't exist
        os.makedirs(self.base_path, exist_ok=True)

    def _get_file_path(self, solution_id: int, language: str) -> Path:
        """Generate the file path for a solution."""
        # Create a filename using the solution ID and language
        filename = f"solution_{solution_id}.{self._get_file_extension(language)}"
        return self.base_path / filename

    def _get_file_extension(self, language: str) -> str:
        """Get the appropriate file extension for a programming language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "cpp": "cpp",
            "c": "c",
            # Add more language mappings as needed
        }
        return extensions.get(language.lower(), "txt")

    def save_solution(self, db: Session, solution: schemas.SolutionCreate) -> models.Solution:
        """Save a solution to both database and filesystem."""
        # First, save to database
        db_solution = models.Solution(
            problem_id=solution.problem_id,
            code=solution.code,
            language=solution.language
        )
        db.add(db_solution)
        db.commit()
        db.refresh(db_solution)

        # Then save to filesystem
        file_path = self._get_file_path(db_solution.id, solution.language)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(solution.code)

        return db_solution

    def load_solution(self, solution_id: int, language: str) -> Optional[str]:
        """Load a solution from the filesystem."""
        file_path = self._get_file_path(solution_id, language)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def delete_solution(self, db: Session, solution_id: int):
        """Delete a solution from both database and filesystem."""
        # Delete from database
        solution = db.query(models.Solution).filter(models.Solution.id == solution_id).first()
        if solution:
            # Delete from filesystem first
            file_path = self._get_file_path(solution_id, solution.language)
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass  # File already doesn't exist
            
            # Then delete from database
            db.delete(solution)
            db.commit()
            return True
        return False
